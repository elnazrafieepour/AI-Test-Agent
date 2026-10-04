from unittest.mock import MagicMock

from app.agent.test_engineer import TestEngineerAgent


def test_agent_analyzes_requirement():

    mock_llm = MagicMock()

    mock_llm.ask.return_value = (
        "Functional scenarios, negative scenarios, "
        "boundary conditions and risks."
    )

    agent = TestEngineerAgent(mock_llm)

    result = agent.analyze_requirement(
        "Users can transfer money between their accounts."
    )

    assert "Functional scenarios" in result

    mock_llm.ask.assert_called_once()