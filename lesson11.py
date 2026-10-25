from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI()

security = HTTPBasic()

EXPECTED_USERNAME = "amar"
EXPECTED_PASSWORD = "python123"


def verify_credentials(
    credentials: HTTPBasicCredentials = Depends(security)
):
    username_correct = secrets.compare_digest(
        credentials.username,
        EXPECTED_USERNAME
    )

    password_correct = secrets.compare_digest(
        credentials.password,
        EXPECTED_PASSWORD
    )

    if not (username_correct and password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@app.get("/")
def home():
    return {"message": "Public endpoint"}


@app.get("/profile")
def profile(username: str = Depends(verify_credentials)):
    return {
        "message": "You are authenticated",
        "username": username
    }