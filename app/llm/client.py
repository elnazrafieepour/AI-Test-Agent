from typing import TypeVar

from pydantic import BaseModel

from app.llm.provider import LLMProvider


T = TypeVar("T", bound=BaseModel)


class LLMClient:

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def ask(self, prompt: str) -> str:
        return self.provider.generate(prompt)

    def ask_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:
        return self.provider.generate_structured(
            prompt,
            response_model,
        )