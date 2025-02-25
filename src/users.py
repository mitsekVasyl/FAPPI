from typing import List, Annotated

from fastapi import Response, status, APIRouter, HTTPException, Depends

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from src.database import SessionDep
from src.models import UserModel
from src.schema import UserRequestSchema, UserBaseSchema, UserQueryParams, USER_ID_PATH_PARAM, UserUpdateSchema

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)

@router.post(
    "/",
    summary="Endpoint to create a new user",
    response_description = "Created user object",
    response_model=UserBaseSchema,
)
def create_user(user: UserRequestSchema, response: Response, dbsession: SessionDep):
    user = UserModel(**user.model_dump())  # TODO: maybe there is another way to map pydantic model into
    dbsession.add(user)                    #  sqlachemy model?
    try:
        dbsession.commit()
    except IntegrityError as ex:
        print(ex.orig)  # TODO: add logging
        if "UNIQUE constraint failed" in str(ex.orig):  # TODO: any other way to distinguish different integrity errors?
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
        raise

    dbsession.refresh(user)
    response.status_code = status.HTTP_201_CREATED
    return user


@router.get(
    "/",
    tags = ["Users"],
    summary = "Endpoint to retrieve users",
    response_description = "List of users",
    response_model=List[UserBaseSchema],
)
def get_users(query_params: Annotated[UserQueryParams, Depends()], response: Response, dbsession: SessionDep):
    """
    Endpoint to retrieve users with request parameters.
    """
    filter_params = query_params.model_dump()
    limit = filter_params.pop("limit")
    filter_conditions = []
    for param, value in filter_params.items():
        if value is not None:
            filter_conditions.append(getattr(UserModel, param) == value)

    if filter_conditions:
        users = dbsession.query(UserModel).filter(and_(*filter_conditions)).limit(limit).all()
    else:
        users = dbsession.query(UserModel).limit(limit).all()

    response.status_code = status.HTTP_200_OK
    return users


@router.get(
    "/{user_id}",
    tags = ["Users"],
    summary = "Endpoint to retrieve user by ID",
    response_description = "User object",
    response_model=UserBaseSchema,
)
def get_user(response: Response, dbsession: SessionDep, user_id: int = USER_ID_PATH_PARAM):
    """
    Endpoint to retrieve user info by user_id.

    **user_id**: required. Path parameter
    """
    user = dbsession.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id=} not found")

    response.status_code = status.HTTP_200_OK
    return user


@router.put(
    "/{user_id}",
    summary = "Endpoint to update user by ID",
    response_description = "Updated user object",
    response_model=UserBaseSchema,
)
def update_user(user: UserUpdateSchema, dbsession: SessionDep, user_id: int = USER_ID_PATH_PARAM):
    existing_user: UserModel = dbsession.query(UserModel).filter(UserModel.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id=} not found")

    for attr, value in user.model_dump().items():
        if value is not None:
            setattr(existing_user, attr, value)

    dbsession.commit()
    dbsession.refresh(existing_user)

    return existing_user
