import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.llm = os.getenv("LLM", "gemini").lower() # default to gemini, options: gemini, anthropic, openai
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.eraserio_api_key = os.getenv("ERASERIO_API_KEY")

config = Config()
