from datetime import datetime
from typing import Optional

import pytz
from pydantic import BaseModel, EmailStr, Field, validator
from typing_extensions import Literal


class UserBase(BaseModel):
    first_name: str = Field(..., max_length=50, min_length=3)
    last_name: str = Field(..., max_length=50, min_length=3)


class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)
    is_active: Literal[1] = 1


class UserUpdate(UserBase):
    old_password: Optional[str] = Field(..., max_length=255)
    new_password: Optional[str] = Field(..., max_length=255)

    @validator("new_password")
    def password_must_be_present_if_old_password_is_present(cls, v, values, **kwargs):
        old_password = values.get("old_password")
        if (old_password and not v) or (not old_password and v):
            raise ValueError("old_password and new_password must be present together")
        return v


class UserInDB(UserBase):
    id: int
    email: str
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDB):
    ...
