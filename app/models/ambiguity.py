from pydantic import BaseModel


class Ambiguity(BaseModel):
    description: str
    question: str