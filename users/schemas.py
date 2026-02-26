from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Annotated


class CreateUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr


class UserSchema(BaseModel):
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True

    model_config = ConfigDict(strict=True)
