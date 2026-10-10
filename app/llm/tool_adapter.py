from app.tools.base.metadata import ToolMetadata


class OpenAIToolAdapter:

    def to_function_tool(
        self,
        metadata: ToolMetadata,
    ) -> dict:

        return {
            "type": "function",
            "name": metadata.name,
            "description": metadata.description,
            "parameters": metadata.input_schema,
            "strict": True,
        }

    def to_function_tools(
        self,
        tools: list[ToolMetadata],
    ) -> list[dict]:

        return [
            self.to_function_tool(tool)
            for tool in tools
        ]