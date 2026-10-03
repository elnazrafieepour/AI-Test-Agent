from unittest.mock import MagicMock, patch

from app.llm.client import LLMClient


def test_llm_client_returns_model_output():

    fake_response = MagicMock()
    fake_response.output_text = "API testing is important."

    with patch("app.llm.client.OpenAI") as mock_openai:

        mock_client = mock_openai.return_value
        mock_client.responses.create.return_value = fake_response

        llm = LLMClient()

        result = llm.ask("Explain API testing.")

        assert result == "API testing is important."