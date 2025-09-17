# overseerr_client.py

import requests
from config import OVERSEERR
from utils import log

class OverseerrClient:
    def __init__(self):
        self.base_url = OVERSEERR["url"].rstrip("/")
        self.api_key = OVERSEERR["api_key"]
        self.session = requests.Session()
        self.session.headers.update({
            "X-Api-Key": self.api_key,
            "Accept": "application/json"
        })

    def get_requests_by_user(self, user_id):
        log(f"Fetching requests for user ID: {user_id}")
        url = f"{self.base_url}/api/v1/request?take=500&sort=added"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()

        user_requests = [
            r for r in data["results"]
            if r["requestedBy"]["id"] == user_id and r["status"] == 2  # APPROVED
        ]

        log(f"Found {len(user_requests)} requests for user ID {user_id}")
        return user_requests
