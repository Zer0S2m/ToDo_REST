from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: Optional[str] = None
    text: str
    pub_date: datetime = datetime.now()
