from fastapi import FastAPI, APIRouter, HTTPException,status
from schemas.task import TaskResponse,TaskRequest

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

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


@router.get("/",response_model=list[TaskResponse])
def read_root():
    return tasks


@router.get("/{task_id}",response_model=TaskResponse)
def read_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")

@router.post("/",response_model=TaskResponse,status_code=status.HTTP_201_CREATED)
def create_task(task_data : TaskRequest):
    new_task = {
        "id": max(task["id"] for task in tasks) + 1,
        "title": task_data.title,
        "status": task_data.status
    }
    tasks.append(new_task)
    return new_task
