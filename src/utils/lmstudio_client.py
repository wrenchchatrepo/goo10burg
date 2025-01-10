import os
from dotenv import load_dotenv
import httpx

load_dotenv()

class LMStudioClient:
    def __init__(self):
        self.api_url = os.environ.get("LMSTUDIO_API_URL")
        if not self.api_url:
            raise Exception("LMSTUDIO_API_URL environment variable not set")
        self.client = httpx.AsyncClient()

    async def generate_text(self, prompt):
        try:
            response = await self.client.post(
                f"{self.api_url}/v1/chat/completions",
                json={
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except httpx.HTTPError as e:
            print(f"Error generating text with LM Studio API: {e}")
            return None
