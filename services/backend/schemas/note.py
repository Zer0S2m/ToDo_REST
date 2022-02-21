from typing import Optional
from typing import Union

from datetime import datetime
from fastapi import File

from pydantic import BaseModel
from pydantic import Field


class NoteSchema(BaseModel):
    id: Optional[int] = Field(None, alias = "idNote")
    title: Optional[str] = Field(None, alias = "titleNote")
    text: Optional[str] = Field(alias = "textNote")
    pub_date: Union[datetime, str] = Field(alias = "pubDate", default = datetime.now())
    id_file: Optional[int] = Field(None, alias = "idFile")
    file_name: Optional[str] = Field(None, alias = "fileName")


class NoteDeleted(BaseModel):
    id: int = Field(alias = "idNote")


class NoteEdit(BaseModel):
    id: Optional[int] = Field(None, alias = "idNote")
    title: Optional[str] = Field(None, alias = "titleNote")
    text: Optional[str] = Field(alias = "textNote")


class FileCreate(BaseModel):
    id: Optional[int] = Field(None, alias = "idFile")
    file_name: Optional[str] = Field(None, alias = "fileName")
