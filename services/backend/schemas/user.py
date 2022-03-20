from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Token(BaseModel):
    access_token: Optional[str] = Field(alias = "accessToken")
    token_type: Optional[str] = Field(alias = "tokenType")


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    ...


class UserInDB(User):
    password: str
    user_id: int
