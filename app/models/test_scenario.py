from typing import Literal

from pydantic import BaseModel


class TestScenario(BaseModel):
    __test__ = False

    title: str
    description: str
    scenario_type: Literal[
        "positive",
        "negative",
        "boundary",
        "validation",
    ]
    priority: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ]