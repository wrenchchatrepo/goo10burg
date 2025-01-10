import requests
import os
from dotenv import load_dotenv

load_dotenv()

class EraserAPI:
    def __init__(self):
        self.api_key = os.environ.get("ERASER_API_KEY")
        if not self.api_key:
            self.api_key = os.getenv("ERASERIO_API_KEY")
        if not self.api_key:
            raise Exception("ERASER_API_KEY environment variable or .env file not set")
        self.base_url = "https://api.eraser.io/v1"


    def get_diagram(self, text):
        url = "https://app.eraser.io/api/render/prompt"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }
        payload = { "text": text }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching diagram from Eraser API: {e}")
            return None
