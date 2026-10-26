
from datetime import datetime, timedelta, timezone
import os

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

# Learning example: configure a real random secret in your environment.
SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "dev-only-change-this-secret-before-deployment"
)
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Demo users only. A real application should use a database.
users = {
    "amar": {
        "username": "amar",
        "role": "user"
    },
    "admin": {
        "username": "admin",
        "role": "admin"
    }
}


def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = users.get(username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user


class user(BaseModel):
    username: str
    role: str

@app.get("/")
def home():
    return {"message": "Public endpoint"}


@app.post("/login")
def login(data: user):
    # Demo only: this endpoint does NOT verify a password.
    # We will focus on role-based authorization in this lesson.
    user = users.get(data.username)

    if user  is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username"
        )

    return {
        "access_token": create_access_token(user["username"]),
        "token_type": "bearer"
    }


@app.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "role": current_user["role"]
    }


@app.get("/admin")
def admin_dashboard(
    current_user: dict = Depends(require_admin)
):
    return {
        "message": "Welcome to the admin dashboard",
        "username": current_user["username"],
        "role": current_user["role"]
    }
