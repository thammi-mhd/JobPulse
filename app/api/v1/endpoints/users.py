from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependency import get_user_repository
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    EmailUpdate,
    PasswordUpdate,
    UserCreate,
    UserEnvelope,
    UserResponse,
    UsersEnvelope,
    UsernameUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


# Use collection/resource routes rather than action names in the URL.
@router.get("/", response_model=UsersEnvelope, status_code=status.HTTP_200_OK)
def get_all_users(
    admin_name: str,
    admin_password: str,
    repository: UserRepository = Depends(get_user_repository),
) -> UsersEnvelope:
    if not admin_name == "admin" or not admin_password == "admin123":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    users = repository.users()
    return UsersEnvelope(
        message="Users retrieved successfully" if users else "No users found",
        users=[UserResponse.model_validate(user) for user in users],
    )


@router.get(
    "/{user_id}",
    response_model=UserEnvelope,
    status_code=status.HTTP_200_OK,
)
def get_user(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
) -> UserEnvelope:
    user = repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserEnvelope(
        message="User retrieved successfully",
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/",
    response_model=UserEnvelope,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    repository: UserRepository = Depends(get_user_repository),
) -> UserEnvelope:
    existing_user = repository.get_user_by_email(user.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    new_user = repository.create_user(
        user.username,
        user.email,
        user.password,
    )
    return UserEnvelope(
        message="User created successfully",
        user=UserResponse.model_validate(new_user),
    )


@router.patch(
    "/{user_id}/username",
    response_model=UserEnvelope,
    status_code=status.HTTP_200_OK,
)
def update_username(
    user_id: int,
    update: UsernameUpdate,
    repository: UserRepository = Depends(get_user_repository),
) -> UserEnvelope:
    user = repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    updated_user = repository.update_username(user, update.new_username)
    return UserEnvelope(
        message="Username updated successfully",
        user=UserResponse.model_validate(updated_user),
    )


@router.patch(
    "/{user_id}/email",
    response_model=UserEnvelope,
    status_code=status.HTTP_200_OK,
)
def update_email(
    user_id: int,
    update: EmailUpdate,
    repository: UserRepository = Depends(get_user_repository),
) -> UserEnvelope:
    user = repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    new_email = str(update.new_email)
    existing_user = repository.get_user_by_email(new_email)
    if existing_user is not None and existing_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    updated_user = repository.update_email(user, new_email)
    return UserEnvelope(
        message="Email updated successfully",
        user=UserResponse.model_validate(updated_user),
    )


@router.patch(
    "/{user_id}/password",
    response_model=UserEnvelope,
    status_code=status.HTTP_200_OK,
)
def update_password(
    user_id: int,
    update: PasswordUpdate,
    repository: UserRepository = Depends(get_user_repository),
) -> UserEnvelope:
    user = repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.hashed_password != update.old_hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password does not match",
        )

    updated_user = repository.update_password(
        user,
        update.old_hashed_password,
        update.new_hashed_password,
    )
    return UserEnvelope(
        message="Password updated successfully",
        user=UserResponse.model_validate(updated_user),
    )


@router.delete(
    "/{user_id}",
    response_model=UserEnvelope,
    status_code=status.HTTP_200_OK,
)
def delete_user(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
) -> UserEnvelope:
    user = repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    response_user = UserResponse.model_validate(user)
    repository.delete_user(user)
    return UserEnvelope(
        message="User deleted successfully",
        user=response_user,
    )
