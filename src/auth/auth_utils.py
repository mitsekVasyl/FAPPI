from bcrypt import gensalt, hashpw, checkpw

def hash_password(password: str) -> bytes:
    return hashpw(password.encode('utf-8'), gensalt())


def verify_password(password: str, hashed_password: bytes) -> bool:
    return checkpw(password.encode('utf-8'), hashed_password)
