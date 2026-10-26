
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

password_hash = PasswordHash.recommended()

SECRET_KEY = "replace-this-with-your-own-random-secret"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 5


# Demo user: store the password hash, never the plain password.
users = {
    "amar": {
        "username": "amar",
        "hashed_password": password_hash.hash("MyPassword123")
    }
}


class LoginRequest(BaseModel):
    username: str
    password: str


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


@app.get("/")
def home():
    return {"message": "Public endpoint"}


@app.post("/login")
def login(data: LoginRequest):
    user = users.get(data.username)

    if user is None or not password_hash.verify(
        data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token(user["username"])

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/profile")
def get_profile(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return {
        "message": "You are authenticated",
        "username": username
    }
