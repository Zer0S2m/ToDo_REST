from datetime import datetime

from typing import (
	Optional, Dict, List
)

from pydantic import BaseModel
from pydantic import Field

from ..note import NoteSchema

from config import (
	LIMIT_TITLE_PART, LIMIT_SLUG_PART, LIMIT_DESCRIPTION_PART,
)


class PartSlug(BaseModel):
	slug: str = Field(max_length = LIMIT_SLUG_PART)


class PartDataStr(BaseModel):
	title: str = Field(max_length = LIMIT_TITLE_PART)
	description: Optional[str] = Field(None, max_length = LIMIT_DESCRIPTION_PART)


class PartBase(PartDataStr, PartSlug):
	pub_date: Optional[datetime] = Field(None, alias = "pubDate")

	class Config:
		allow_population_by_field_name = True
		orm_mode = True


class PartSchema(PartBase):
	id: int
	notes: List[NoteSchema]


class PartList(PartBase):
	id: int
	count_notes: int = Field(alias = "countNotes")
	count_notes_importance_levels: Dict[int, int] = Field(None, alias = "countNotesImportanceLevels")


class PartCreate(PartBase):
	id_project: int = Field(alias = "idProject")


class PartDeleted(PartSlug):
	...


class PartInProject(PartSlug):
	id: int
	title: str = Field(max_length = LIMIT_TITLE_PART)


class PartEdit(PartDataStr):
	id: int

	class Config:
		allow_population_by_field_name = True
		orm_mode = True
