from typing import List

from pydantic import BaseModel
from pydantic import Field

from config import (
    LIMIT_CATEGORY_TITLE, LIMIT_CATEGORY_SLUG
)


class CategoryBase(BaseModel):
    slug: str = Field(max_length = LIMIT_CATEGORY_SLUG)


class CategorySchema(CategoryBase):
    title: str = Field(max_length = LIMIT_CATEGORY_TITLE)


class CategoryCreate(CategorySchema):
    ...


class CategoryDelete(CategoryBase):
    ...


class CategoryList(BaseModel):
    categories: List[CategorySchema]
