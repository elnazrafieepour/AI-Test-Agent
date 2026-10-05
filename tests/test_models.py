import pytest
from pydantic import ValidationError

from app.models.requirement_analysis import RequirementAnalysis


def test_requirement_analysis_accepts_valid_data():

    analysis = RequirementAnalysis(
        test_scenarios=[
            {
                "title": "Successful transfer",
                "description": "Transfer money between two valid accounts.",
                "scenario_type": "positive",
                "priority": "high",
            }
        ],
        risks=[
            {
                "description": "Duplicate transaction",
                "severity": "critical",
            }
        ],
        ambiguities=[
            {
                "description": "Maximum transfer amount is undefined.",
                "question": "What is the maximum allowed amount?",
            }
        ],
    )

    assert len(analysis.test_scenarios) == 1
    assert analysis.test_scenarios[0].priority == "high"
    assert analysis.risks[0].severity == "critical"


def test_requirement_analysis_rejects_invalid_scenario_type():

    with pytest.raises(ValidationError):

        RequirementAnalysis(
            test_scenarios=[
                {
                    "title": "Invalid scenario",
                    "description": "Invalid scenario type.",
                    "scenario_type": "unknown",
                    "priority": "high",
                }
            ],
            risks=[],
            ambiguities=[],
        )