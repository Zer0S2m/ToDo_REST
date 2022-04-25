from typing import Optional
from pydantic import BaseModel
from pydantic import Field

from config import (
	LIMIT_CATEGORY_TITLE, LIMIT_CATEGORY_SLUG
)


class CategoryBase(BaseModel):
	slug: str = Field(max_length = LIMIT_CATEGORY_SLUG)
	project_id: int = Field(alias = "projectId")

	class Config:
		allow_population_by_field_name = True
		orm_mode = True


class CategorySchemaCreate_Main(CategoryBase):
	title: str = Field(max_length = LIMIT_CATEGORY_TITLE)


class CategorySchema(CategorySchemaCreate_Main):
	id: int


class CategoryCreate(CategorySchemaCreate_Main):
	...


class CategoryDelete(BaseModel):
	slug: str = Field(max_length = LIMIT_CATEGORY_SLUG)


class CategorySchemeInNote(BaseModel):
	id: Optional[int]
	slug: Optional[str] = Field(None, max_length = LIMIT_CATEGORY_SLUG)
	title: Optional[str] = Field(None, max_length = LIMIT_CATEGORY_TITLE)
