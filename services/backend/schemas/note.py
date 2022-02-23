from typing import (
    Optional, Union, List
)

from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class BaseNote(BaseModel):
    id: Optional[int] = Field(None, alias = "idNote")
    title: Optional[str] = Field(None, alias = "titleNote")
    text: Optional[str] = Field(alias = "textNote")
    file_name: Optional[str] = Field(None, alias = "fileName")


class NoteSchema(BaseNote, BaseModel):
    pub_date: Union[datetime, str] = Field(alias = "pubDate", default = datetime.now())


class NoteList(BaseModel):
    notes: List[NoteSchema]


class NoteDeleted(BaseModel):
    id: Optional[int] = Field(alias = "idNote")


class NoteEdit(BaseNote, BaseModel):
    id: Optional[int] = Field(alias = "idNote")
