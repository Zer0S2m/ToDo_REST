from typing import (
    Optional, Union, List
)

from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from config import (
    LIMIT_NOTE_TEXT, LIMIT_NOTE_TITLE
)


class BaseNote(BaseModel):
    title: Optional[str] = Field(None, alias = "titleNote", max_length = LIMIT_NOTE_TITLE)
    text: Optional[str] = Field(alias = "textNote", max_length = LIMIT_NOTE_TEXT)
    pub_date: Optional[datetime] = Field(alias = "pubDate", default = datetime.now())
    category_slug: Optional[str] = Field(None, alias = "categorySlug")
    importance: Optional[int] = Field(None)


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
