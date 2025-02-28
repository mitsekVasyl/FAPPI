from os import getenv
from datetime import datetime, timezone, timedelta

from bcrypt import gensalt, hashpw, checkpw
from jose import jwt

SECRET = getenv("JWT_SECRET")
ALGO = "HS256"
TOKEN_PREFIX = "Bearer "


def hash_password(password: str) -> bytes:
    return hashpw(password.encode('utf-8'), gensalt())


def verify_password(password: str, hashed_password: bytes) -> bool:
    return checkpw(password.encode('utf-8'), hashed_password)


def generate_access_token(username: str, user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    data = {"exp": expires, "user_id": user_id, "username": username}
    return TOKEN_PREFIX + jwt.encode(data, key=SECRET, algorithm=ALGO)
