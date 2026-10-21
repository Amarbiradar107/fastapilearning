from typing import Literal

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field

app = FastAPI()

tasks = [
    {"id": 101, "title": "Learn FastAPI", "status": "pending"},
    {"id": 102, "title": "Practice Python", "status": "completed"},
    {"id": 103, "title": "Build a REST API", "status": "pending"},
    {"id": 104, "title": "Learn PostgreSQL", "status": "in progress"},
    {"id": 105, "title": "Deploy to Heroku", "status": "pending"},
    {"id": 106, "title": "Write Unit Tests", "status": "completed"},
    {"id": 107, "title": "Implement Authentication", "status": "in progress"},
    {"id": 108, "title": "Optimize Performance", "status": "pending"},
    {"id": 109, "title": "Refactor Codebase", "status": "completed"},
    {"id": 110, "title": "Document API Endpoints", "status": "in progress"},
    {"id": 111, "title": "Integrate Third-Party APIs", "status": "pending"},
    {"id": 112, "title": "Set Up CI/CD Pipeline", "status": "completed"},
    {"id": 113, "title": "Implement Caching", "status": "in progress"},
    {"id": 114, "title": "Conduct Code Reviews", "status": "pending"},
    {"id": 115, "title": "Monitor Application Performance", "status": "completed"},
    {"id": 116, "title": "Implement Logging", "status": "in progress"}
]



class PatchUpdate(BaseModel):
    title : str | None = Field(default=None, min_length=3, max_length=50)
    status: Literal["pending","in progress","completed"] | None = None


class PutUpdate(BaseModel):
    title : str = Field(min_length=3, max_length=50)
    status: Literal["pending","in progress","completed"] = "pending"


@app.put("/tasks/{task_id}")
def update_task(task_id:int, taskupdate:PutUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = taskupdate.title
            task["status"] = taskupdate.status
            return task
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")


@app.patch("/tasks/{task_id}")
def update_task(task_id:int, taskupdate:PatchUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if taskupdate.title is not None:
                task["title"] = taskupdate.title
            if taskupdate.status is not None:
                task["status"] = taskupdate.status
            return task
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")


