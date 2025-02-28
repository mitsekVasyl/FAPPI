from bcrypt import gensalt, hashpw

def hash_password(password: str) -> bytes:
    return hashpw(password.encode('utf-8'), gensalt())
