import pytest

from app.tools.openapi.tool import OpenAPITool
from app.tools.registry import ToolRegistry


def test_register_and_get_tool():
    registry = ToolRegistry()
    tool = OpenAPITool()
    registry.register(tool)
    result = registry.get(
        "openapi_parser"
    )
    assert result is tool


def test_register_duplicate_tool():
    registry = ToolRegistry()
    registry.register(
        OpenAPITool()
    )
    with pytest.raises(
            ValueError,
            match="Tool already registered",
    ):
        registry.register(
            OpenAPITool()
        )


def test_get_unknown_tool():
    registry = ToolRegistry()
    with pytest.raises(
            KeyError,
            match="Tool not found",
    ):
        registry.get(
            "unknown_tool"
        )


def test_list_tools():
    registry = ToolRegistry()
    tool = OpenAPITool()
    registry.register(tool)
    tools = registry.list_tools()
    assert len(tools) == 1
    assert tools[0] is tool


def test_execute_tool():
    registry = ToolRegistry()
    registry.register(
        OpenAPITool()
    )
    result = registry.execute(
        "openapi_parser",
        "tests/fixtures/openapi/transfer_api.yaml",
    )
    assert result.title == "Transfer API"
    assert len(result.endpoints) == 1


def test_discover_tools():
    registry = ToolRegistry()
    registry.register(
        OpenAPITool()
    )
    tools = registry.discover()
    assert len(tools) == 1
    metadata = tools[0]
    assert metadata.name == "openapi_parser"
    assert (
            "OpenAPI"
            in metadata.description
    )
