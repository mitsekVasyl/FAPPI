from os import getenv
from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from bcrypt import gensalt, hashpw, checkpw
from jose import jwt, JWTError


SECRET = getenv("JWT_SECRET")
ALGO = "HS256"
TOKEN_PREFIX = "Bearer "

bearer_dep = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def hash_password(password: str) -> bytes:
    return hashpw(password.encode('utf-8'), gensalt())


def verify_password(password: str, hashed_password: bytes) -> bool:
    return checkpw(password.encode('utf-8'), hashed_password)


def generate_access_token(username: str, user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    data = {"exp": expires, "user_id": user_id, "username": username}
    return TOKEN_PREFIX + jwt.encode(data, key=SECRET, algorithm=ALGO)


def verify_access_token(token: Annotated[str, Depends(bearer_dep)]) -> dict:
    try:
        user_info = jwt.decode(token, key=SECRET, algorithms=[ALGO])
        return user_info
    except JWTError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed access token verification") from ex
