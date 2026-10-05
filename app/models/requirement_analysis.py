from pydantic import BaseModel

from app.models.ambiguity import Ambiguity
from app.models.risk import Risk
from app.models.test_scenario import TestScenario


class RequirementAnalysis(BaseModel):
    test_scenarios: list[TestScenario]
    risks: list[Risk]
    ambiguities: list[Ambiguity]