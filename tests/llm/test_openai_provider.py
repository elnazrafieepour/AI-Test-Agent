
import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.llm.openai_provider import OpenAIProvider


def make_response(
    output,
    output_text="",
    response_id="resp_test",
):
    return SimpleNamespace(
        output=output,
        output_text=output_text,
        id=response_id,
    )


def make_function_call(
    name="openapi_parser",
    arguments=None,
    call_id="call_test",
):
    if arguments is None:
        arguments = {"file_path": "openapi.yaml"}

    return SimpleNamespace(
        type="function_call",
        name=name,
        arguments=json.dumps(arguments),
        call_id=call_id,
    )


def make_provider(responses):
    provider = OpenAIProvider.__new__(OpenAIProvider)
    provider.client = MagicMock()
    provider.model = "test-model"
    provider.client.responses.create.side_effect = responses
    return provider

TOOLS = [
    {
        "type": "function",
        "name": "openapi_parser",
        "description": "Parse an OpenAPI file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"}
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def test_returns_direct_response_without_executing_tool():
    response = make_response(
        output=[],
        output_text="No tool is needed.",
    )
    provider = make_provider([response])
    executor = MagicMock()

    result = provider.generate_with_tools(
        prompt="Explain what API testing is.",
        tools=TOOLS,
        executor=executor,
    )

    assert result == "No tool is needed."
    executor.execute.assert_not_called()
    assert provider.client.responses.create.call_count == 1


def test_executes_tool_and_returns_final_response():
    function_call = make_function_call(
        arguments={
            "file_path": "tests/fixtures/openapi/transfer_api.yaml"
        },
        call_id="call_123",
    )

    first_response = make_response(
        output=[function_call],
        response_id="resp_1",
    )

    final_response = make_response(
        output=[],
        output_text="The API contains a transfer endpoint.",
        response_id="resp_2",
    )

    provider = make_provider(
        [first_response, final_response]
    )

    executor = MagicMock()
    executor.execute.return_value = {
        "title": "Transfer API",
        "endpoint_count": 1,
    }

    result = provider.generate_with_tools(
        prompt="Analyze the transfer API.",
        tools=TOOLS,
        executor=executor,
    )

    assert result == "The API contains a transfer endpoint."

    executor.execute.assert_called_once_with(
        "openapi_parser",
        {
            "file_path": (
                "tests/fixtures/openapi/transfer_api.yaml"
            )
        },
    )

    calls = provider.client.responses.create.call_args_list

    assert calls[1].kwargs["previous_response_id"] == "resp_1"

    tool_outputs = calls[1].kwargs["input"]

    assert len(tool_outputs) == 1
    assert tool_outputs[0]["type"] == "function_call_output"
    assert tool_outputs[0]["call_id"] == "call_123"

    returned_output = json.loads(
        tool_outputs[0]["output"]
    )

    assert returned_output["ok"] is True
    assert returned_output["result"]["title"] == "Transfer API"


def test_returns_tool_error_to_model():
    function_call = make_function_call()

    first_response = make_response(
        output=[function_call],
        response_id="resp_1",
    )

    final_response = make_response(
        output=[],
        output_text="The file could not be parsed.",
        response_id="resp_2",
    )

    provider = make_provider(
        [first_response, final_response]
    )

    executor = MagicMock()
    executor.execute.side_effect = ValueError(
        "Invalid OpenAPI file"
    )

    result = provider.generate_with_tools(
        prompt="Analyze the API.",
        tools=TOOLS,
        executor=executor,
    )

    assert result == "The file could not be parsed."

    tool_outputs = (
        provider.client.responses.create
        .call_args_list[1]
        .kwargs["input"]
    )

    returned_output = json.loads(
        tool_outputs[0]["output"]
    )

    assert returned_output["ok"] is False
    assert returned_output["error"]["type"] == "ValueError"
    assert returned_output["error"]["message"] == (
        "Invalid OpenAPI file"
    )


def test_rejects_unknown_tool_name():
    function_call = make_function_call(
        name="delete_production_database",
        call_id="call_unknown",
    )

    first_response = make_response(
        output=[function_call],
        response_id="resp_1",
    )

    final_response = make_response(
        output=[],
        output_text="The requested tool is not allowed.",
        response_id="resp_2",
    )

    provider = make_provider(
        [first_response, final_response]
    )

    executor = MagicMock()

    result = provider.generate_with_tools(
        prompt="Analyze the API.",
        tools=TOOLS,
        executor=executor,
    )

    assert result == "The requested tool is not allowed."
    executor.execute.assert_not_called()

    tool_outputs = (
        provider.client.responses.create
        .call_args_list[1]
        .kwargs["input"]
    )

    returned_output = json.loads(
        tool_outputs[0]["output"]
    )

    assert returned_output["ok"] is False
    assert returned_output["error"]["type"] == "ValueError"


def test_stops_after_maximum_tool_rounds():
    responses = []

    for index in range(6):
        responses.append(
            make_response(
                output=[
                    make_function_call(
                        call_id=f"call_{index}"
                    )
                ],
                response_id=f"resp_{index}",
            )
        )

    provider = make_provider(responses)
    executor = MagicMock()
    executor.execute.return_value = {"ok": True}

    with pytest.raises(
        RuntimeError,
        match="Maximum tool-calling rounds exceeded",
    ):
        provider.generate_with_tools(
            prompt="Analyze the API.",
            tools=TOOLS,
            executor=executor,
        )

    assert executor.execute.call_count == 5
    assert provider.client.responses.create.call_count == 6
