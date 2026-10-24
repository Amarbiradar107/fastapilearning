from typing import Literal

from pydantic import BaseModel, Field


class TaskResponse(BaseModel):
    id :int
    title : str
    status:Literal["pending", "in progress", "completed"]

class TaskRequest(BaseModel):
    title :str = Field(min_length=3)
    status:Literal["pending", "in progress", "completed"]="pending"
