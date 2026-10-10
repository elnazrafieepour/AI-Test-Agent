from typing import Any, Protocol


class Tool(Protocol):

    @property
    def name(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    def input_schema(self) -> dict[str, Any]:
        ...

    def execute(self, input_data: Any) -> Any:
        ...
