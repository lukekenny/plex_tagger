# config.py

# Plex server settings
PLEX = {
    "url": "http://plex.smallcreek.com.au:32400",
    "token": "tHPyyN1Xoq78AM2aDWYP"
}

# Radarr server settings
RADARR = {
    "url": "http://radarr.smallcreek.com.au:7878",
    "api_key": "fb2f9dc5fd524ca59a1a0e69071c1e88"
}

# Sonarr server settings
SONARR = {
    "url": "http://sonarr.smallcreek.com.au:8989",
    "api_key": "083874ac45b04643a047e9201815ec6a"
}

# Overseerr server settings
OVERSEERR = {
    "url": "https://overseerr.smallcreek.com.au",
    "api_key": "MTcxOTA0MDYxODAzMmE5MGVjMjFhLTVkZTMtNGRkZS1iMGMyLThlMDBhNWY2ZWIyNg=="
}

# Flask server host and port
SERVER = {
    "host": "0.0.0.0",
    "port": 13131
}

# TMDb API credentials
TMDB_API_KEY = "34a23d943ad31593827ed325499c1f30"
TMDB_READ_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNGEyM2Q5NDNhZDMxNTkzODI3ZWQzMjU0OTljMWYzMCIsIm5iZiI6MTc1Mzc5NTI4MS40MTEsInN1YiI6IjY4ODhjYWQxNTg1NTk3YzEwMGY3OWQ2NSIsInNjb3BlcyJdLCJ2ZXJzaW9uIjoxfQ.3qE3QqrQUCdNydXW2iCYmV19L8mdzFq9vdscIK4Gvko"

# User tagging configuration
USER_TAGS = {
    "2": {
        "username": "leesa_8",
        "tag": "2 - leesa_8",
        "movie_collection": "Leesa's Movies",
        "tv_collection": "Leesa's Series"
    },
    "1": {
        "username": "lukekenny",
        "tag": "1 - lukekenny",
        "movie_collection": "Luke's Movies",
        "tv_collection": "Luke's Series"
    }
}

# The user to run the tagging for
CONFIGURED_USER = "lukekenny"
