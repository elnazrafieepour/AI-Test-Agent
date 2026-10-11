from unittest.mock import MagicMock

from app.llm.client import LLMClient



from unittest.mock import MagicMock

from app.llm.client import LLMClient


def test_llm_client_returns_model_output():
    mock_provider = MagicMock()
    mock_provider.generate.return_value = (
        "API testing is important."
    )

    llm = LLMClient(mock_provider)

    result = llm.ask("Explain API testing.")

    assert result == "API testing is important."
    mock_provider.generate.assert_called_once_with(
        "Explain API testing."
    )


def test_llm_client_sends_prompt_to_model():
    mock_provider = MagicMock()
    mock_provider.generate.return_value = "Test response"

    llm = LLMClient(mock_provider)

    result = llm.ask("Generate API test cases.")

    mock_provider.generate.assert_called_once_with(
        "Generate API test cases."
    )
    assert result == "Test response"
