from pydantic import BaseModel


class ToolMetadata(BaseModel):

    name: str
    description: str