import logging
import json
from flask import Flask, request
from config import SERVER, OVERSEERR, USER_TAGS, PLEX
from tagging import tag_item_to_collection, notify_plex

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler() # Also log to console
        ]
    )

app = Flask(__name__)
app.debug = False

@app.route("/health", methods=["POST"])
def health():
    return "OK", 200

@app.route("/radarr", methods=["POST"])
def radarr_webhook():
    payload = request.json
    title = payload.get("movie", {}).get("title")
    tmdb_id = payload.get("movie", {}).get("tmdbId")
    moviePath = payload.get("movie", {}).get("folderPath")
    app.logger.info(f"Received Radarr webhook for movie {title} (TMDb ID: {tmdb_id})")
    if int(tmdb_id) == 0:
        return "OK", 200
    if tmdb_id is not None:
        notify_plex("movie", moviePath)
        tag_item_to_collection("movie", int(tmdb_id), title)
    return "", 204

@app.route("/sonarr", methods=["POST"])
def sonarr_webhook():
    payload = request.json
    title = payload.get("series", {}).get("title")
    tmdb_id = payload.get("series", {}).get("tmdbId")
    seriesPath = payload.get("series", {}).get("path")
    app.logger.info(f"Received Sonarr webhook for series {title} (TMDb ID: {tmdb_id})")
    if int(tmdb_id) == 0:
        return "OK", 200
    if tmdb_id is not None:
        notify_plex("series", seriesPath)
        tag_item_to_collection("series", int(tmdb_id), title)
    return "", 204

if __name__ == "__main__":
    host = SERVER.get("host", "0.0.0.0")
    port = SERVER.get("port", 13131)
    app.run(host=host, port=port)
