from pathlib import Path
import yaml
import pytest

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

def test_parse_file_raises_error_for_missing_file():

    parser = OpenAPIParser()

    missing_file = Path(
        "tests/fixtures/openapi/not_found.yaml"
    )

    with pytest.raises(
        FileNotFoundError,
        match="OpenAPI file not found",
    ):
        parser.parse_file(missing_file)

def test_parse_multiple_endpoints():

    document = {
        "openapi": "3.1.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "paths": {
            "/users": {
                "get": {
                    "summary": "Get users",
                    "responses": {
                        "200": {
                            "description": "Success"
                        }
                    },
                },
                "post": {
                    "summary": "Create user",
                    "responses": {
                        "201": {
                            "description": "Created"
                        }
                    },
                },
            }
        },
    }

    parser = OpenAPIParser()

    result = parser.parse(document)

    assert len(result.endpoints) == 2

    methods = {
        endpoint.method
        for endpoint in result.endpoints
    }

    assert methods == {"GET", "POST"}


def test_parse_parameter():

    document = {
        "openapi": "3.1.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "paths": {
            "/accounts/{account_id}": {
                "get": {
                    "parameters": [
                        {
                            "name": "account_id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "string"
                            },
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Success"
                        }
                    },
                }
            }
        },
    }

    result = OpenAPIParser().parse(document)

    endpoint = result.endpoints[0]

    assert len(endpoint.parameters) == 1

    parameter = endpoint.parameters[0]

    assert parameter.name == "account_id"
    assert parameter.location == "path"
    assert parameter.required is True
    assert parameter.schema.type == "string"

def test_parse_schema_constraints():

    document = {
        "openapi": "3.1.0",
        "info": {
            "title": "Transfer API",
            "version": "1.0.0",
        },
        "paths": {
            "/transfers": {
                "post": {
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "number",
                                    "minimum": 1,
                                    "maximum": 10_000_000,
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Success"
                        }
                    },
                }
            }
        },
    }

    result = OpenAPIParser().parse(document)

    endpoint = result.endpoints[0]

    schema = endpoint.request_body.schema

    assert schema.type == "number"
    assert schema.minimum == 1
    assert schema.maximum == 10_000_000

def test_parse_invalid_yaml():

    parser = OpenAPIParser()

    file_path = Path(
        "tests/fixtures/openapi/invalid.yaml"
    )

    with pytest.raises(
        yaml.YAMLError
    ):
        parser.parse_file(file_path)