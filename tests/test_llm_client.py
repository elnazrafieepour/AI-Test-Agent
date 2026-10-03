from unittest.mock import MagicMock

from app.llm.client import LLMClient


def test_llm_client_returns_model_output():
    fake_response = MagicMock()
    fake_response.output_text = "API testing is important."

    mock_client = MagicMock()
    mock_client.responses.create.return_value = fake_response

    llm = LLMClient(mock_client)

    result = llm.ask("Explain API testing.")

    assert result == "API testing is important."

    mock_client.responses.create.assert_called_once_with(
        model="gpt-5",
        input="Explain API testing."
    )


def test_llm_client_sends_prompt_to_model():
    mock_client = MagicMock()

    fake_response = MagicMock()
    fake_response.output_text = "Test response"

    mock_client.responses.create.return_value = fake_response

    llm = LLMClient(mock_client)

    llm.ask("Generate API test cases.")

    mock_client.responses.create.assert_called_once_with(
        model="gpt-5",
        input="Generate API test cases."
    )
