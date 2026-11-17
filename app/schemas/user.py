from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="The username of the user")
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(..., min_length=8, description="The password for the user")


class UsernameUpdate(BaseModel):
    new_username: str = Field(..., min_length=1, max_length=50)


class EmailUpdate(BaseModel):
    new_email: EmailStr


class PasswordUpdate(BaseModel):
    old_hashed_password: str
    new_hashed_password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# These envelopes keep every endpoint's documented response aligned with its payload.
class UserEnvelope(BaseModel):
    message: str
    user: UserResponse


class UsersEnvelope(BaseModel):
    message: str
    users: list[UserResponse]