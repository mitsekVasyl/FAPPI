from typing import List, Annotated

from fastapi import Response, status, APIRouter, HTTPException, Depends

from sqlalchemy.exc import IntegrityError

from src.auth.auth_utils import verify_access_token, authorize_user_request
from src.database import SessionDep
from src.models import UserModel
from src.schema import UserCreateSchema, UserResponseSchema, UserQueryParams, USER_ID_PATH_PARAM, UserUpdateSchema
from src import users_persister

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)

@router.post(
    "/",
    summary="Endpoint to create a new user",
    response_description = "Created user object",
    response_model=UserResponseSchema,
    responses={
        status.HTTP_409_CONFLICT: {"description": "User already exists"},
    }
)
def create_user(user: UserCreateSchema, response: Response, dbsession: SessionDep):
    try:
        user = users_persister.save_user(dbsession, UserModel(**user.model_dump()))
    except IntegrityError as ex:
        print(ex.orig)  # TODO: add logging
        if "UNIQUE constraint failed" in str(ex.orig):  # TODO: any other way to distinguish different integrity errors?
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
        raise
    response.status_code = status.HTTP_201_CREATED
    return user


@router.get(
    "/",
    tags = ["Users"],
    summary = "Endpoint to retrieve users",
    response_description = "List of users",
    response_model=List[UserResponseSchema],
)
def get_users(query_params: Annotated[UserQueryParams, Depends()], response: Response, dbsession: SessionDep,
              user_info: Annotated[dict, Depends(verify_access_token)]):
    """
    Endpoint to retrieve users with request parameters.
    """
    filter_params = query_params.model_dump()
    if not user_info.get("is_admin", False): # hide other users for regular users
        filter_params.update({"id": user_info["user_id"]})

    users = users_persister.query_users(dbsession, filter_params)

    response.status_code = status.HTTP_200_OK
    return users


@router.get(
    "/{user_id}",
    tags = ["Users"],
    summary = "Endpoint to retrieve user by ID",
    response_description = "User object",
    response_model=UserResponseSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    }
)
def get_user(response: Response, dbsession: SessionDep, user_info: Annotated[dict, Depends(verify_access_token)],
             user_id: Annotated[int, USER_ID_PATH_PARAM]):
    """
    Endpoint to retrieve user info by user_id.

    **user_id**: required. Path parameter
    """
    authorize_user_request(user_id, user_info)

    user = users_persister.query_user(dbsession, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id=} not found")

    response.status_code = status.HTTP_200_OK
    return user


@router.put(
    "/{user_id}",
    summary = "Endpoint to update user by ID",
    response_description = "Updated user object",
    response_model=UserResponseSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    }
)
def update_user(user: UserUpdateSchema, dbsession: SessionDep, user_info: Annotated[dict, Depends(verify_access_token)],
                user_id: Annotated[int, USER_ID_PATH_PARAM]):
    authorize_user_request(user_id, user_info)

    existing_user = users_persister.query_user(dbsession, user_id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id=} not found")

    users_persister.update_user(dbsession, user, existing_user)

    return existing_user


@router.delete(
    "/{user_id}",
    summary = "Endpoint to delete user by ID",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    }
)
def delete_user(response: Response, dbsession: SessionDep, user_info: Annotated[dict, Depends(verify_access_token)],
                user_id: Annotated[int, USER_ID_PATH_PARAM]):
    authorize_user_request(user_id, user_info)

    existing_user = users_persister.query_user(dbsession, user_id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id=} not found")

    users_persister.delete_user(dbsession, existing_user)

    response.status_code = status.HTTP_204_NO_CONTENT
    return {"message": "No Content"}
