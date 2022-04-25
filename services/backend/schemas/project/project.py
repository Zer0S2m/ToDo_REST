from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from .comment import CommentSchema
from .part import (
	PartList, PartInProject
)
from ..category import CategorySchema

from config import (
	LIMIT_TITLE_PROJECT, LIMIT_SLUG_PROJECT,
	LIMIT_DESCRIPTION_PROJECT,
)


class ProjectBase(BaseModel):
	title: str = Field(max_length = LIMIT_TITLE_PROJECT)
	slug: str = Field(max_length = LIMIT_SLUG_PROJECT)
	description: Optional[str] = Field(None, max_length = LIMIT_DESCRIPTION_PROJECT)
	pub_date: Optional[datetime] = Field(None, alias = "pubDate")

	class Config:
		allow_population_by_field_name = True
		orm_mode = True


class ProjectSchema(ProjectBase):
	id: int
	parts: List[PartList] = Field(None)
	comments: List[CommentSchema] = Field(None)
	categories: List[CategorySchema] = Field(None)


class ProjectMain(ProjectBase):
	id: int
	parts: List[PartInProject] = Field(None)
	comments: List[CommentSchema] = Field(None)
	categories: List[CategorySchema] = Field(None)


class ProjectCreate(ProjectBase):
	...


class ProjectDeleted(BaseModel):
	slug: str = Field(max_length = LIMIT_SLUG_PROJECT)
