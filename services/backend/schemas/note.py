from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class NoteSchema(BaseModel):
    id: Optional[int] = Field(None, alias = "idNote")
    title: Optional[str] = Field(None, alias = "titleNote")
    text: Optional[str] = Field(alias = "textNote")
    pub_date: Optional[datetime] = Field(alias = "pubDate", default = datetime.now())


class NoteDeleted(BaseModel):
    note_id: int = Field(alias = "noteId")
