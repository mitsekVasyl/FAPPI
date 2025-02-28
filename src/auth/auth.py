from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.auth_utils import verify_password, generate_access_token
from src.database import SessionDep
from src.models import UserModel


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)


@router.post("/token")
def get_token(form: Annotated[OAuth2PasswordRequestForm, Depends()], dbsesssion: SessionDep):
    user = dbsesssion.query(UserModel).filter(UserModel.username == form.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    is_authenticated = verify_password(form.password, user.password)
    if not is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return {"access_token": generate_access_token(user.username, user.id),
            "token_type": "Bearer"}
