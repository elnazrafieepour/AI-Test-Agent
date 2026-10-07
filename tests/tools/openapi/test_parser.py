from pathlib import Path

from app.tools.openapi.models import OpenAPISpec
from app.tools.openapi.parser import OpenAPIParser


FIXTURE = Path(
    "tests/fixtures/openapi/transfer_api.yaml"
)


def test_parse_openapi_file():

    parser = OpenAPIParser()

    result = parser.parse_file(FIXTURE)

    assert isinstance(result, OpenAPISpec)

    assert result.title == "Transfer API"
    assert result.version == "1.0.0"
    assert result.openapi_version == "3.1.0"

    assert result.servers == [
        "https://api.example.com"
    ]

    assert len(result.endpoints) == 1

    endpoint = result.endpoints[0]

    assert endpoint.method == "POST"
    assert endpoint.path == "/transfers"
    assert endpoint.operation_id == "createTransfer"