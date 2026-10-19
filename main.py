
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to my first FastAPI application!"}

#just commenting to test the commit functionality