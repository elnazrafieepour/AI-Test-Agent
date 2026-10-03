from openai import OpenAI

from app.config import settings
from app.llm.client import LLMClient


def create_llm_client() -> LLMClient:
    client = OpenAI(
        api_key=settings.openai_api_key
    )

    return LLMClient(client)