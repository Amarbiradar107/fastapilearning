from typing import Literal

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    status: Literal["pending", "in progress", "completed"] = "pending"


class TaskResponse(BaseModel):
    id: int
    title: str
    status: Literal["pending", "in progress", "completed"]
    comment : str = "added by amar"