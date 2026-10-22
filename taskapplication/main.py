from fastapi import FastAPI

from routers.tasks import router as tasks_router

app = FastAPI(title="Task Management API")

app.include_router(tasks_router)


@app.get("/")
def home():
    return {"message": "Task Management API is running"}