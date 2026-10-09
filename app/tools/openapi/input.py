from pydantic import BaseModel, ConfigDict, Field


class OpenAPIInput(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    file_path: str = Field(
        min_length=1,
        description="Path to the OpenAPI YAML or JSON file.",
    )