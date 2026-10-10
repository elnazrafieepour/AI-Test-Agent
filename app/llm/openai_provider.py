
import json
from typing import Any, TypeVar

from openai import OpenAI
from pydantic import BaseModel

from app.llm.provider import ToolExecutorProtocol


T = TypeVar("T", bound=BaseModel)


class OpenAIProvider:

    def __init__(self):
        # Load settings only when the provider is instantiated.
        from app.config import settings

        self.client = OpenAI(
            api_key=settings.openai_api_key
        )
        self.model = settings.openai_model

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:

        response = self.client.responses.parse(
            model=self.model,
            input=prompt,
            text_format=response_model,
        )

        result = response.output_parsed

        if result is None:
            raise ValueError(
                "LLM did not return a structured response."
            )

        return result

    def generate_with_tools(
        self,
        prompt: str,
        tools: list[dict[str, Any]],
        executor: ToolExecutorProtocol,
    ) -> str:

        if not tools:
            return self.generate(prompt)

        allowed_tool_names = {
            tool["name"]
            for tool in tools
        }

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            tools=tools,
            tool_choice="auto",
        )

        tool_rounds = 0
        max_tool_rounds = 5

        while True:

            function_calls = [
                item
                for item in response.output
                if item.type == "function_call"
            ]

            if not function_calls:
                return response.output_text

            if tool_rounds >= max_tool_rounds:
                raise RuntimeError(
                    "Maximum tool-calling rounds exceeded."
                )

            tool_rounds += 1
            tool_outputs = []

            for function_call in function_calls:

                tool_name = function_call.name

                try:
                    if tool_name not in allowed_tool_names:
                        raise ValueError(
                            f"Tool is not allowed: {tool_name}"
                        )

                    arguments = json.loads(
                        function_call.arguments
                    )

                    if not isinstance(arguments, dict):
                        raise ValueError(
                            "Tool arguments must be a JSON object."
                        )

                    result = executor.execute(
                        tool_name,
                        arguments,
                    )

                    if isinstance(result, BaseModel):
                        result = result.model_dump(
                            mode="json"
                        )

                    output = {
                        "ok": True,
                        "result": result,
                    }

                except Exception as exc:
                    output = {
                        "ok": False,
                        "error": {
                            "type": type(exc).__name__,
                            "message": str(exc),
                        },
                    }

                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": function_call.call_id,
                        "output": json.dumps(
                            output,
                            ensure_ascii=False,
                            default=str,
                        ),
                    }
                )

            response = self.client.responses.create(
                model=self.model,
                previous_response_id=response.id,
                input=tool_outputs,
                tools=tools,
                tool_choice="auto",
            )
