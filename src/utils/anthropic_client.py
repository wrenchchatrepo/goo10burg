import os
import asyncio
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

class AnthropicClient:
    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise Exception("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=self.api_key)

    async def generate_text(self, prompt):
        try:
            response = await asyncio.to_thread(
                self.client.completions.create,
                model="claude-2",
                max_tokens_to_sample=1024,
                prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
            )
            return response.completion
        except Exception as e:
            print(f"Error generating text with Anthropic API: {e}")
            return None
