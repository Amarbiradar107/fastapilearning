
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

password_hash = PasswordHash.recommended()

# Learning example only. Use a random secret from an environment variable
# in real applications.
SECRET_KEY = "replace-this-with-your-own-random-secret"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 5

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = users.get(username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {"username": user["username"]}


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
def profile(current_user: dict = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "username": current_user["username"]
    }
