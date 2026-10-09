from pathlib import Path

import pytest

from app.tools.executor import ToolExecutor
from app.tools.openapi.models import OpenAPISpec
from app.tools.openapi.tool import OpenAPITool
from app.tools.registry import ToolRegistry


FIXTURE = Path(
    "tests/fixtures/openapi/transfer_api.yaml"
)


def test_executor_runs_registered_tool():
    registry = ToolRegistry()
    registry.register(OpenAPITool())
    executor = ToolExecutor(registry)
    result = executor.execute(
        "openapi_parser",
        FIXTURE,
    )
    assert isinstance(result, OpenAPISpec)
    assert result.title == "Transfer API"
    assert len(result.endpoints) == 1


def test_executor_rejects_unknown_tool():
    executor = ToolExecutor(
        ToolRegistry()
    )
    with pytest.raises(
        KeyError,
        match="Tool not found",
    ):
        executor.execute(
            "unknown_tool",
            {},
        )