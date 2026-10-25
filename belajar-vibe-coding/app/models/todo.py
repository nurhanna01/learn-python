from pydantic import BaseModel, Field


class Todo(BaseModel):
    id: int
    title: str
    completed: bool = Field(default=False)
