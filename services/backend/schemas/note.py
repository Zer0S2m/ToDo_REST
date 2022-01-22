from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class NoteSchema(BaseModel):
    title: Optional[str] = None
    text: str
    pub_date: Optional[datetime] = Field(alias = "pubDate", default = datetime.now())


class NoteDeleted(BaseModel):
    note_id: int = Field(alias = "noteId")
