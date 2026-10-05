from typing import Literal

from pydantic import BaseModel


class Risk(BaseModel):
    description: str
    severity: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ]