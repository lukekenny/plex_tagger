# list_users.py

import requests
from config import OVERSEERR
from utils import log

def list_users():
    url = f"{OVERSEERR['url'].rstrip('/')}/api/v1/user"
    headers = {
        "X-Api-Key": OVERSEERR["api_key"],
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    users = data.get("results", data)  # Try "results" field first, then fallback
    if isinstance(users, list):
        for user in users:
            log(f"User ID: {user.get('id')} | Plex Username: {user.get('plexUsername')} | Email: {user.get('email')}")
    else:
        log("Unexpected response format:")
        print(data)

if __name__ == "__main__":
    list_users()
