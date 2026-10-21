
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TaskCreate(BaseModel):
    title: str
    status: str = "pending"


tasks = []


@app.post("/tasks")
def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "status": task.status
    }

    tasks.append(new_task)

    return new_task
