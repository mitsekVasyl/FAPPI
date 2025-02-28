from operator import and_
from typing import List, Optional, Type

from sqlalchemy.orm import Session

from src.auth.auth_utils import hash_password
from src.models import UserModel
from src.schema import UserUpdateSchema


def save_user(db: Session, user: UserModel) -> UserModel:
    user.password = hash_password(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def query_user(db: Session, user_id: int) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def query_users(db: Session, filter_params: dict) -> List[Type[UserModel]]:
    limit = filter_params.pop("limit")
    filter_conditions = []
    for param, value in filter_params.items():
        if value is not None:
            filter_conditions.append(getattr(UserModel, param) == value)

    if filter_conditions:
        users = db.query(UserModel).filter(and_(*filter_conditions)).limit(limit).all()
    else:
        users = db.query(UserModel).limit(limit).all()

    return users


def update_user(db: Session, user: UserUpdateSchema, existing_user: UserModel) -> None:
    # TODO: handle cases when value is intentionally None
    for attr, value in user.model_dump().items():
        if value is not None:
            setattr(existing_user, attr, value)

    db.commit()
    db.refresh(existing_user)


def delete_user(db: Session, user: UserModel) -> None:
    db.delete(user)
    db.commit()
