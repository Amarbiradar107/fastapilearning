
from fastapi import FastAPI

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


@app.get("/")
def home():
    return {"message": "Welcome to my Task Management API!"}


@app.get("/tasks")
def get_tasks(status: str | None = None, limit: int = 10):
    filtered_tasks = tasks
    if status is not None:
        # filtered_tasks = [ task for task in filtered_tasks if task["status"] == status]
        filtered_tasks = []
        for task in tasks:
            if task["status"]==status:
                filtered_tasks.append(task)

        if not filtered_tasks:
            return {"message": "No tasks found with the specified status."}

    return filtered_tasks[:limit]



@app.get("/tasks/search")
def search_title(title :str | None = None):
    filtered_tasks = tasks

    if title is not None:
        filtered_tasks = []
        for task in tasks:
            if title.lower() in task["title"].lower():
                filtered_tasks.append(task)
    if not filtered_tasks:
        return {"message": "No tasks found with the specified title."}

    return filtered_tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return {"message": "Task not found"}



