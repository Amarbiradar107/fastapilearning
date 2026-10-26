from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Learning example only. Generate your own secret key.
SECRET_KEY = "test"

# openssl rand -hex 32
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 1440


def create_access_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/token")
def login():
    token = create_access_token("AMAR")

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/profile")
def get_profile(token: str = Depends(oauth2_scheme)):
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "message": "You are authenticated",
        "username": username
    }