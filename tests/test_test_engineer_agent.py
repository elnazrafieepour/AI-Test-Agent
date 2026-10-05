from unittest.mock import MagicMock
import pytest
from app.agent.test_engineer import TestEngineerAgent
from app.models.requirement_analysis import RequirementAnalysis
from app.validation.requirement_validator import (
    RequirementAnalysisValidator,
)


def test_agent_analyzes_requirement():

    mock_llm = MagicMock()

    expected_analysis = RequirementAnalysis(
        requirement_summary=(
            "Users can transfer money between "
            "their own accounts."
        ),
        test_scenarios=[
            {
                "title": "Successful transfer",
                "description": (
                    "Transfer money between valid accounts."
                ),
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
                "description": (
                    "Maximum transfer amount is undefined."
                ),
                "question": (
                    "What is the maximum transfer amount?"
                ),
            }
        ],
    )

    mock_llm.ask_structured.return_value = (
        expected_analysis
    )

    mock_validator = MagicMock(
        spec=RequirementAnalysisValidator
    )

    mock_validator.validate.return_value = []

    agent = TestEngineerAgent(
        mock_llm,
        mock_validator,
    )

    result = agent.analyze_requirement(
        "Users can transfer money between their accounts."
    )

    assert isinstance(
        result,
        RequirementAnalysis,
    )

    assert result.requirement_summary

    assert len(result.test_scenarios) == 1

    assert (
        result.test_scenarios[0].scenario_type
        == "positive"
    )

    assert (
        result.risks[0].severity
        == "critical"
    )

    mock_llm.ask_structured.assert_called_once()

    mock_validator.validate.assert_called_once_with(
        expected_analysis
    )


def test_agent_rejects_invalid_analysis():

    mock_llm = MagicMock()

    invalid_analysis = RequirementAnalysis(
        requirement_summary="Transfer requirement.",
        test_scenarios=[],
        risks=[],
        ambiguities=[],
    )

    mock_llm.ask_structured.return_value = (
        invalid_analysis
    )

    mock_validator = MagicMock(
        spec=RequirementAnalysisValidator
    )

    mock_validator.validate.return_value = [
        "At least one test scenario is required."
    ]

    agent = TestEngineerAgent(
        mock_llm,
        mock_validator,
    )

    with pytest.raises(
        ValueError,
        match="Requirement analysis validation failed",
    ):
        agent.analyze_requirement(
            "Users can transfer money."
        )