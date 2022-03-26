from typing import (
    Optional, Union, List
)

from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class BaseNote(BaseModel):
    title: Optional[str] = Field(None, alias = "titleNote")
    text: Optional[str] = Field(alias = "textNote")
    pub_date: Union[datetime, str] = Field(alias = "pubDate", default = datetime.now())
    category_slug: Optional[str] = Field(None, alias = "categorySlug")


class NoteSchema(BaseNote):
    id: Optional[int] = Field(None, alias = "idNote")
    file_name: Union[bool, str] = Field(None, alias = "fileName")


class NoteCreate(BaseNote):
    ...


class NoteList(BaseModel):
    notes: List[NoteSchema]


class NoteDeleted(BaseModel):
    id: Optional[int] = Field(alias = "idNote")


class NoteEdit(BaseNote):
    id: Optional[int] = Field(alias = "idNote")
    file_name: Union[bool, str] = Field(None, alias = "fileName")
