import requests
import time
from flask import current_app
from plexapi.server import PlexServer
from config import PLEX, USER_TAGS, OVERSEERR

# Initialize Plex connection
plex = PlexServer(PLEX["url"], PLEX["token"])

def get_requester_and_media_info(media_type, external_id):
    headers = {"X-Api-Key": OVERSEERR["api_key"]}
    if media_type == "movie":
        url = f"{OVERSEERR['url']}/api/v1/movie/{external_id}"
        plex_library = plex.library.section('Movies')
    else:
        url = f"{OVERSEERR['url']}/api/v1/tv/{external_id}"
        plex_library = plex.library.section('Series')
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    json_data = resp.json()
    media_info = json_data.get("mediaInfo") or json_data
    requests_list = media_info.get("requests", [])
    if not requests_list:
        return None, None
    first_req = requests_list[0]
    user_id = first_req.get("requestedBy", {}).get("id")
    #rating_key = media_info.get("ratingKey")
    plex_search = f"tmdb://{external_id}"

    # We may need to try a few times before Plex indexs the file

    max_retries = 10

    for attempt in range(max_retries):
        try:
            current_app.logger.info(f"Searching Plex for {plex_search}")
            plex_item = plex_library.getGuid(plex_search)
            current_app.logger.debug(f"Returned plex_item: {plex_item}")
            rating_key = plex_item.ratingKey
            current_app.logger.info(f"ratingKey {rating_key} found.")
            return user_id, rating_key
        except:
            if attempt < max_retries - 1:
                current_app.logger.error(f"{plex_search} not in Plex library yet.  Waiting 5 seconds.  Attempt {attempt + 1} of {max_retries}")
                time.sleep(5)
            else:
                current_app.logger.error(f"{plex_search} not in Plex library.  Operation failed.")
                return None, None

def tag_item_to_collection(media_type, external_id, title):
    user_id, rating_key = get_requester_and_media_info(media_type, external_id)
    current_app.logger.info(f"Requester: {user_id} - ratingKey {rating_key}")
    if not user_id or not rating_key:
        current_app.logger.warning(f"Skipping tagging for {title}: no Overseerr request or ratingKey.")
        return

    # USER_TAGS keys are strings of user IDs
    user_config = USER_TAGS.get(str(user_id))
    if not user_config:
        current_app.logger.error(f"No USER_TAGS config for user ID {user_id}")
        return
    collection_name = user_config["movie_collection"] if media_type == "movie" else user_config["tv_collection"]
    try:
        item = plex.fetchItem(rating_key)
        item.addCollection(collection_name)
        current_app.logger.info(f"    -> Tagged '{item.title}' into collection '{collection_name}'")
    except Exception as e:
        current_app.logger.error(f"    -> Failed to tag '{title}' into collection '{collection_name}': {e}")
    return

def notify_plex(media_type, destinationPath):
    current_app.logger.info(f"Plex Notification: {media_type} - {destinationPath}")
    if media_type == "movie":
        #notify_library = plex.library.section('Movies')
        notify_library = plex.library.sectionByID(5)
    else:
        #notify_library = plex.library.section('Series')
        notify_library = plex.library.sectionByID(4)
    notify_library.update(destinationPath)
    current_app.logger.info(f"Plex notified to scan library... waiting 5 seconds...")
    time.sleep(5)
    return
