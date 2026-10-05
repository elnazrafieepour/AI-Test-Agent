from unittest.mock import MagicMock

from app.agent.test_engineer import TestEngineerAgent
from app.models.requirement_analysis import RequirementAnalysis


def test_agent_analyzes_requirement():

    mock_llm = MagicMock()

    expected_analysis = RequirementAnalysis(
        test_scenarios=[
            {
                "title": "Successful transfer",
                "description": "Transfer money between valid accounts.",
                "scenario_type": "positive",
                "priority": "high",
            }
        ],
        risks=[
            {
                "description": "Duplicate transaction.",
                "severity": "critical",
            }
        ],
        ambiguities=[
            {
                "description": "Maximum transfer amount is undefined.",
                "question": "What is the maximum transfer amount?",
            }
        ],
    )

    mock_llm.ask_structured.return_value = expected_analysis

    agent = TestEngineerAgent(mock_llm)

    result = agent.analyze_requirement(
        "Users can transfer money between their accounts."
    )

    assert isinstance(result, RequirementAnalysis)

    assert len(result.test_scenarios) == 1

    assert result.test_scenarios[0].scenario_type == "positive"

    assert result.risks[0].severity == "critical"

    mock_llm.ask_structured.assert_called_once()