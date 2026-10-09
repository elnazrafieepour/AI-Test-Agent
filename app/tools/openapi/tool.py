from pathlib import Path

from app.tools.openapi.input import OpenAPIInput
from app.tools.openapi.models import OpenAPISpec
from app.tools.openapi.parser import OpenAPIParser


class OpenAPITool:

    @property
    def name(self) -> str:
        return "openapi_parser"

    @property
    def description(self) -> str:
        return (
            "Parse an OpenAPI YAML or JSON file "
            "into a structured API specification."
        )

    def input_schema(self) -> dict:
        return OpenAPIInput.model_json_schema()

    def execute(
        self,
        input_data: dict,
    ) -> OpenAPISpec:

        validated_input = OpenAPIInput.model_validate(
            input_data
        )

        parser = OpenAPIParser()

        return parser.parse_file(
            Path(validated_input.file_path)
        )