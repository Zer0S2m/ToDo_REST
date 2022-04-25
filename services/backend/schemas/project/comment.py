from typing import Optional

from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from config import LIMIT_TEXT_COMMENT


class CommentBase(BaseModel):
	text: str = Field(max_length = LIMIT_TEXT_COMMENT)
	pub_date: Optional[datetime] = Field(None, alias = "pubDate")

	class Config:
		allow_population_by_field_name = True
		orm_mode = True


class CommentSchema(CommentBase):
	id: int


class CommentCreate(CommentBase):
	id_project: int = Field(alias = "idProject")


class CommentDeleted(BaseModel):
	id: int


class CommentEdit(CommentSchema):
	...
