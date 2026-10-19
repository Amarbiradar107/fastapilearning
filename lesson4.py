from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    status: Literal["pending", "in progress", "completed"] = "pending"

@app.post("/tasks")
def create_task(task: TaskCreate):
    return {
        "title": task.title,
        "status": task.status
    }