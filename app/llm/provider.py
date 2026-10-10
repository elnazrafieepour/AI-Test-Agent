
from typing import Any, Protocol, TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class ToolExecutorProtocol(Protocol):

    def execute(
        self,
        tool_name: str,
        input_data: Any,
    ) -> Any:
        ...


class LLMProvider(Protocol):

    def generate(self, prompt: str) -> str:
        ...

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:
        ...

    def generate_with_tools(
        self,
        prompt: str,
        tools: list[dict[str, Any]],
        executor: ToolExecutorProtocol,
    ) -> str:
        ...
