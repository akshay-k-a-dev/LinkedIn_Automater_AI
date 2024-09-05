# src/gemini_api_client.py

import requests

class GeminiAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.gemini.com/v1"  # Replace with the actual API URL

    def request(self, endpoint, payload):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{self.api_url}/{endpoint}", json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
