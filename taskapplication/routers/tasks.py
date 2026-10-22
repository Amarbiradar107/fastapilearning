from fastapi import APIRouter, HTTPException, status

from schemas.task import TaskCreate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "status": "pending"
    },
    {
        "id": 2,
        "title": "Practice Python",
        "status": "completed"
    }
]


@router.get("/", response_model=list[TaskResponse])
def get_tasks():
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(task_data: TaskCreate):
    new_task = {
        "id": max((task["id"] for task in tasks), default=0) + 1,
        "title": task_data.title,
        "status": task_data.status
    }

    tasks.append(new_task)
    return new_task