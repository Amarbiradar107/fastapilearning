from fastapi import FastAPI
from routers.tasks import router as tasks_router

app = FastAPI(title="Task Application")

app.include_router(tasks_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Task Application!"}
