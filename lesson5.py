from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TaskCreate(BaseModel):
    title: str
    status: str = "pending"
    detail: str = "This is a task detail"


class TaskResponse(BaseModel):
    id: int
    title: str
    # detail: str = "This is a task detail"
    status: str



@app.post("/tasks", response_model=TaskResponse,status_code=201)
def create_task(task: TaskCreate):
    new_task = {
        "id": 1,
        "title": task.title,
        "status": task.status,
        # "detail": task.detail,
        "internal_note": "This should not be exposed"
    }

    return new_task