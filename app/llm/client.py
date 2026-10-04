from app.config import settings
from app.llm.provider import LLMProvider


class LLMClient:

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def ask(self, prompt: str) -> str:
        return self.provider.generate(prompt)