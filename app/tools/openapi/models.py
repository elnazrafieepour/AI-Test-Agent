from pydantic import BaseModel, Field
from typing import Any, Literal


class APIParameter(BaseModel):
    name: str
    location: Literal[
        "query",
        "path",
        "header",
        "cookie",
    ]
    required: bool = False
    schema: APISchema | None = None
    description: str | None = None
    example: Any = None


class APIRequestBody(BaseModel):
    required: bool = False
    content_type: str | None = None
    schema: APISchema | None = None
    example: Any = None
    description: str | None = None


class APIResponse(BaseModel):
    status_code: str
    description: str
    content_type: str | None = None
    schema: APISchema | None = None
    example: Any = None

class OpenAPISpec(BaseModel):
    title: str
    version: str
    openapi_version: str
    servers: list[str] = Field(
        default_factory=list
    )
    endpoints: list[APIEndpoint] = Field(
        default_factory=list
    )


class APISchema(BaseModel):
    type: str | None = None
    format: str | None = None

    required: bool = False

    minimum: float | None = None
    maximum: float | None = None
    min_length: int | None = None
    max_length: int | None = None

    pattern: str | None = None

    enum: list[Any] = Field(
        default_factory=list
    )

    example: Any = None


class APISecurity(BaseModel):
    scheme_name: str
    scheme_type: str
    scopes: list[str] = Field(
        default_factory=list
    )


class APIEndpoint(BaseModel):
    method: Literal[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "HEAD",
        "OPTIONS",
        "TRACE",
    ]
    path: str
    operation_id: str | None = None
    summary: str | None = None
    description: str | None = None
    tags: list[str] = Field(
        default_factory=list
    )
    parameters: list[APIParameter] = Field(
        default_factory=list
    )
    request_body: APIRequestBody | None = None
    responses: list[APIResponse] = Field(
        default_factory=list
    )
    security: list[APISecurity] = Field(
        default_factory=list
    )
    deprecated: bool = False