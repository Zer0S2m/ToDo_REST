from typing import Optional

from datetime import datetime

from pydantic import (
	BaseModel, Field
)

from config import (
	LIMIT_NOTE_TEXT, LIMIT_NOTE_TITLE
)

from .category import CategorySchemeInNote


class IdNote(BaseModel):
	id: int = Field(alias = "idNote")


class BaseNote(BaseModel):
	title: Optional[str] = Field(None, alias = "titleNote", max_length = LIMIT_NOTE_TITLE)
	text: str = Field(alias = "textNote", max_length = LIMIT_NOTE_TEXT)
	pub_date: datetime = Field(alias = "pubDate", default = datetime.now())
	importance: Optional[int] = Field(None)
	part_id: int = Field(alias = "partId")
	project_id: int = Field(alias = "projectId")

	class Config:
		allow_population_by_field_name = True
		orm_mode = True


class NoteSchema(BaseNote, IdNote):
	file_name: Optional[str] = Field(None, alias = "fileName")
	active: bool
	category: Optional[CategorySchemeInNote] = Field(None)


class NoteCreate(BaseNote):
	category_id: Optional[int] = Field(None, alias = "categoryId")


class NoteDeleted(IdNote):
	...


class NoteEdit(IdNote, BaseNote):
	file_name: Optional[str] = Field(None, alias = "fileName")
	category_id: Optional[int] = Field(None, alias = "categoryId")


class NoteComplete(IdNote):
	...
