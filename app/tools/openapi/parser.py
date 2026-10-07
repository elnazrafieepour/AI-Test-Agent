from pathlib import Path

import yaml

from app.tools.openapi.models import (
    APIEndpoint,
    APIParameter,
    APIResponse,
    APIRequestBody,
    APISchema,
    APISecurity,
    OpenAPISpec,
)


class OpenAPIParser:

    def parse_file(self, file_path: str | Path) -> OpenAPISpec:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"OpenAPI file not found: {path}"
            )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            document = yaml.safe_load(file)

        return self.parse(document)

    def parse(self, document: dict) -> OpenAPISpec:

        info = document.get("info", {})

        endpoints = []

        for path, path_item in document.get(
            "paths",
            {},
        ).items():

            for method, operation in path_item.items():

                if method.lower() not in {
                    "get",
                    "post",
                    "put",
                    "patch",
                    "delete",
                    "head",
                    "options",
                    "trace",
                }:
                    continue

                endpoint = self._parse_endpoint(
                    method=method,
                    path=path,
                    operation=operation,
                )

                endpoints.append(endpoint)

        return OpenAPISpec(
            title=info.get(
                "title",
                "Unknown API",
            ),
            version=info.get(
                "version",
                "Unknown",
            ),
            openapi_version=document.get(
                "openapi",
                "Unknown",
            ),
            servers=[
                server.get("url", "")
                for server in document.get(
                    "servers",
                    [],
                )
            ],
            endpoints=endpoints,
        )

    def _parse_endpoint(
        self,
        method: str,
        path: str,
        operation: dict,
    ) -> APIEndpoint:

        return APIEndpoint(
            method=method.upper(),
            path=path,
            operation_id=operation.get("operationId"),
            summary=operation.get("summary"),
            description=operation.get("description"),
            tags=operation.get("tags", []),
            parameters=self._parse_parameters(
                operation.get("parameters", [])
            ),
            request_body=self._parse_request_body(
                operation.get("requestBody")
            ),
            responses=self._parse_responses(
                operation.get("responses", {})
            ),
            security=self._parse_security(
                operation.get("security", [])
            ),
            deprecated=operation.get(
                "deprecated",
                False,
            ),
        )

    def _parse_parameters(
        self,
        parameters: list[dict],
    ) -> list[APIParameter]:

        result = []

        for parameter in parameters:

            schema_data = parameter.get(
                "schema",
                {},
            )

            schema = self._parse_schema(
                schema_data
            )

            result.append(
                APIParameter(
                    name=parameter["name"],
                    location=parameter["in"],
                    required=parameter.get(
                        "required",
                        False,
                    ),
                    schema=schema,
                    description=parameter.get(
                        "description"
                    ),
                    example=parameter.get(
                        "example"
                    ),
                )
            )

        return result

    def _parse_schema(
        self,
        schema_data: dict,
    ) -> APISchema:

        return APISchema(
            type=schema_data.get("type"),
            format=schema_data.get("format"),
            required=schema_data.get(
                "required",
                False,
            ),
            minimum=schema_data.get(
                "minimum"
            ),
            maximum=schema_data.get(
                "maximum"
            ),
            min_length=schema_data.get(
                "minLength"
            ),
            max_length=schema_data.get(
                "maxLength"
            ),
            pattern=schema_data.get(
                "pattern"
            ),
            enum=schema_data.get(
                "enum",
                [],
            ),
            example=schema_data.get(
                "example"
            ),
        )

    def _parse_request_body(
        self,
        request_body: dict | None,
    ) -> APIRequestBody | None:

        if request_body is None:
            return None

        content = request_body.get(
            "content",
            {},
        )

        if not content:
            return APIRequestBody(
                required=request_body.get(
                    "required",
                    False,
                ),
                description=request_body.get(
                    "description"
                ),
            )

        content_type, media_type = next(
            iter(content.items())
        )

        schema_data = media_type.get(
            "schema",
            {},
        )

        return APIRequestBody(
            required=request_body.get(
                "required",
                False,
            ),
            content_type=content_type,
            schema=self._parse_schema(
                schema_data
            ),
            example=media_type.get(
                "example"
            ),
            description=request_body.get(
                "description"
            ),
        )

    def _parse_responses(
        self,
        responses: dict,
    ) -> list[APIResponse]:

        result = []

        for status_code, response in responses.items():

            content = response.get(
                "content",
                {},
            )

            content_type = None
            schema = None
            example = None

            if content:

                content_type, media_type = next(
                    iter(content.items())
                )

                schema_data = media_type.get(
                    "schema",
                    {}
                )

                schema = self._parse_schema(
                    schema_data
                )

                example = media_type.get(
                    "example"
                )

            result.append(
                APIResponse(
                    status_code=str(
                        status_code
                    ),
                    description=response.get(
                        "description",
                        "",
                    ),
                    content_type=content_type,
                    schema=schema,
                    example=example,
                )
            )

        return result

    def _parse_security(
        self,
        security: list[dict],
    ) -> list[APISecurity]:

        result = []

        for requirement in security:

            for scheme_name, scopes in requirement.items():

                result.append(
                    APISecurity(
                        scheme_name=scheme_name,
                        scheme_type="unknown",
                        scopes=scopes,
                    )
                )

        return result

