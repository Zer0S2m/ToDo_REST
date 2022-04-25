from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from config import LIMIT_USERNAME


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	username: Optional[str] = None


class UserBase(BaseModel):
	username: str = Field(max_length = LIMIT_USERNAME)
	email: Optional[str] = None


class UserCreate(UserBase):
	password: str


class User(UserBase):
	...


class UserInDB(User):
	password: str
	user_id: int
