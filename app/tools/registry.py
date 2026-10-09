from typing import Any

from app.tools.base.metadata import ToolMetadata
from app.tools.base.tool import Tool


##responsibility of this class: register new tool in agent; get a tool; list of tools; introduce ability of tools to agent (discovery); excute tool.
class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:

        if name not in self._tools:
            raise KeyError(
                f"Tool not found: {name}"
            )

        return self._tools[name]

    ##get the implimentation of tools:
    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def execute(
            self,
            name: str,
            input_data: Any,
    ) -> Any:

        tool = self.get(name)

        return tool.execute(input_data)

    ##help to agent for select a fit tool:
    def discover(self) -> list[ToolMetadata]:
        return [
            ToolMetadata(
                name=tool.name,
                description=tool.description,
            )
            for tool in self._tools.values()
        ]
