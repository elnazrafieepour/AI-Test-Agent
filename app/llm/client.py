from openai import OpenAI

from app.config import settings


class LLMClient:

    def __init__(self, client: OpenAI):
        self.client = client

    def ask(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=settings.openai_model,
            input=prompt
        )

        return response.output_text