import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
from src.config import config
from src.utils.anthropic_client import AnthropicClient
from src.utils.openrouter_client import OpenRouterClient
from src.utils.lmstudio_client import LMStudioClient

load_dotenv()

class GeminiAPI:
    def __init__(self):
        self.llm = config.llm
        if self.llm == "gemini":
            self.api_key = config.gemini_api_key
            if not self.api_key:
                raise Exception("GEMINI_API_KEY environment variable not set")
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-pro')
        elif self.llm == "anthropic":
            self.client = AnthropicClient()
        elif self.llm == "openai":
            self.api_key = config.openai_api_key
            if not self.api_key:
                raise Exception("OPENAI_API_KEY environment variable not set")
            self.client = OpenAI(api_key=self.api_key)
        elif self.llm == "openrouter":
            self.client = OpenRouterClient()
        elif self.llm == "lmstudio":
            self.client = LMStudioClient()
        else:
            raise Exception(f"Invalid LLM specified in config: {self.llm}")


    async def generate_text(self, prompt):
        try:
            if self.llm == "gemini":
                print("Sending request to Gemini API...")
                response = await asyncio.to_thread(self.client.generate_content, prompt)
                print("Received response from Gemini API")
                return response.text
            elif self.llm == "openai":
                chat_completion = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="gpt-3.5-turbo",
                )
                return chat_completion.choices[0].message.content
            elif self.llm == "anthropic":
                return await self.client.generate_text(prompt)
            elif self.llm == "openrouter":
                return await self.client.generate_text(prompt)
            elif self.llm == "lmstudio":
                return await self.client.generate_text(prompt)
            else:
                raise Exception(f"Invalid LLM specified in config: {self.llm}")
        except Exception as e:
            print(f"Error generating text with Gemini API: {e}")
            return None

    async def generate_article_content(self, metadata):
        prompt = f"Generate a technical article based on the following metadata: {metadata}"
        return await self.generate_text(prompt)

    async def generate_script_content(self, metadata):
        prompt = f"Generate a technical script based on the following metadata: {metadata}"
        return await self.generate_text(prompt)
