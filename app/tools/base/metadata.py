from typing import Any
from pydantic import BaseModel, ConfigDict, Field

class ToolMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str

    input_schema: dict[str, Any] = Field(
        default_factory=dict
    )
