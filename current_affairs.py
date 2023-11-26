import requests
import time
import logging
from config import RAPID_API_KEY, RAPID_API_HOST


class CurrentAffairs:
    def _make_request(self, endpoint):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error {response.status_code}: {response.text}")
        time.sleep(15)

    def get(self, key):
        item = self.items[key]
        if item == None:
            logging.error("An Error Occurred Fetching Item", key)
        if len(item) == 0:
            logging.error(f"No {key} available")
            return None
        return item

    def __init__(self):
        self.base_url: str = "https://current-affairs-of-india.p.rapidapi.com/"
        self.items = {}
        endpoints = {
            "recent": "recent",
            "history": "history-of-today",
            "quiz": "today-quiz",
            "international": "international-today",
        }
        for key, value in endpoints.items():
            response = self._make_request(value)
            if key == "history":
                response = response[-5:]
            self.items[key] = response

    def _get_headers(self) -> dict[str, str]:
        return {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_API_HOST}

    def get_recent_current_affairs(self) -> list[str]:
        """
        Returns a list of current affairs
        Has around 6 items
        """
        return self.get("recent")

    def get_history_of_today(self) -> list[dict]:
        """
        Returns a list of dict with keys:
        - date: str
        - description: str
        """
        return self.get("history")

    def get_today_quiz(self) -> list[dict]:
        """
        Returns a list of dict with one key:
        - question: str
        """
        return self.get("quiz")

    def get_international_current_affairs(self) -> list[dict]:
        return self.get("international")
