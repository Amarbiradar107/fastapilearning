from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Demo token only — not for production use
DEMO_TOKEN = "fastapi-demo-token"


@app.post("/token")
def login():
    # For this lesson, return a fixed demo token.
    # Real login must verify a user's credentials first.
    return {
        "access_token": DEMO_TOKEN,
        "token_type": "bearer"
    }


@app.get("/")
def home():
    return {"message": "Public endpoint"}


@app.get("/profile")
def get_profile(token: str = Depends(oauth2_scheme)):
    if token != DEMO_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return {
        "message": "You are authenticated",
        "token_type": "bearer"
    }