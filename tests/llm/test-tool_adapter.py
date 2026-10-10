from app.llm.tool_adapter import OpenAIToolAdapter
from app.tools.base.metadata import ToolMetadata


def test_convert_metadata_to_function_tool():

    metadata = ToolMetadata(
        name="openapi_parser",
        description="Parse an OpenAPI specification.",
        input_schema={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                },
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
    )

    adapter = OpenAIToolAdapter()

    result = adapter.to_function_tool(metadata)

    assert result["type"] == "function"
    assert result["name"] == "openapi_parser"
    assert result["strict"] is True

    assert (
        result["parameters"]["required"]
        == ["file_path"]
    )


def test_convert_multiple_function_tools():

    tools = [
        ToolMetadata(
            name="openapi_parser",
            description="Parse OpenAPI.",
            input_schema={"type": "object"},
        ),
        ToolMetadata(
            name="another_tool",
            description="Another tool.",
            input_schema={"type": "object"},
        ),
    ]

    adapter = OpenAIToolAdapter()

    result = adapter.to_function_tools(tools)

    assert len(result) == 2
    assert result[0]["name"] == "openapi_parser"
    assert result[1]["name"] == "another_tool"