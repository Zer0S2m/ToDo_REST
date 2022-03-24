from typing import List

from pydantic import BaseModel


class CategoryBase(BaseModel):
    slug: str


class CategorySchema(CategoryBase):
    title: str


class CategoryCreate(CategorySchema):
    ...


class CategoryDelete(CategoryBase):
    ...


class CategoryList(BaseModel):
    categories: List[CategorySchema]
