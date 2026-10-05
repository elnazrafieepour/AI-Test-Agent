from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel

from app.config import settings


T = TypeVar("T", bound=BaseModel)


class OpenAIProvider:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=settings.openai_model,
            input=prompt,
        )

        return response.output_text

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:

        response = self.client.responses.parse(
            model=settings.openai_model,
            input=prompt,
            text_format=response_model,
        )

        result = response.output_parsed

        if result is None:
            raise ValueError(
                "LLM did not return a structured response."
            )

        return result