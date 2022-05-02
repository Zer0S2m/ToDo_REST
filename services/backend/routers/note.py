from typing import List

from fastapi import (
	APIRouter, HTTPException, UploadFile,
	Depends, File, status
)
from fastapi.responses import StreamingResponse

from schemas.user import UserInDB
from schemas.note import (
	NoteSchema, NoteDeleted, NoteEdit,
	NoteCreate, NoteComplete
)

from models import Note

from utils.db.category import ServiceDBCategory

from utils.db.note import (
	set_file_note, get_file, ServiceDBNote
)
from utils.users import get_current_user
from utils.common import (
	set_category_note, set_file_name_note, check_is_project_in_db
)


router = APIRouter(
	prefix = "/project/{slug_project:str}/note",
	tags = ["project", "note"],
	responses = {404: {"description": "Not found"}},
	dependencies = [Depends(check_is_project_in_db)]
)


async def check_is_note_in_db(
	note_id: int,
	service: ServiceDBNote
) -> Note:
	note = await service.fetch_one(note_id)
	if not note:
		raise HTTPException(status_code = 404, detail = "Note not found")
	return note


@router.get(
	"/",
	response_model = List[NoteSchema],
	response_model_exclude_unset = True
)
async def get_notes(
	slug_project: str,
	service: ServiceDBNote = Depends()
) -> List[dict]:
	notes = []

	notes_db = await service.fetch_all(slug_project)
	for note in notes_db:
		note_dict = set_category_note(note = note)
		note_dict = set_file_name_note(note = note, note_dict = note_dict)
		notes.append(note_dict)

	return notes


@router.get(
	"/{note_id:int}",
	response_model = NoteSchema,
	response_model_exclude = ("file_id")
)
async def get_note(
	slug_project: str,
	note_id: int,
	service: ServiceDBNote = Depends()
) -> dict:
	note = await check_is_note_in_db(note_id, service)
	note_dict = set_category_note(note = note)
	note_dict = set_file_name_note(note = note, note_dict = note_dict)

	return note_dict


@router.delete("/delete")
async def delete_note(
	slug_project: str,
	note: NoteDeleted,
	service: ServiceDBNote = Depends()
):
	await check_is_note_in_db(note.id, service)
	await service.delete(note)


@router.put(
	"/edit",
	response_model = NoteSchema
)
async def edit_note(
	slug_project: str,
	note: NoteEdit = Depends(),
	file: UploadFile = File(None),
	service: ServiceDBNote = Depends()
)-> dict:
	await check_is_note_in_db(note.id, service)

	data_file = {}
	if file:
		data_file = await set_file_note(file, service.current_user)

	note = await service.edit(note, data_file)
	note_dict = note.as_dict
	note_dict = set_category_note(note = note)

	return note_dict


@router.patch(
	"/complete"
)
async def complete_note(
	slug_project: str,
	note: NoteComplete,
	service: ServiceDBNote = Depends()
):
	await check_is_note_in_db(note.id, service)
	await service.complete(note)


@router.post(
	"/create",
	response_model = NoteSchema,
	status_code = status.HTTP_201_CREATED
)
async def create_note(
	slug_project: str,
	note: NoteCreate = Depends(),
	file: UploadFile = File(None),
	service_category: ServiceDBCategory = Depends(),
	service_note: ServiceDBNote = Depends()
) -> dict:
	file_id = 0
	file_name = None

	if file:
		data_file = await set_file_note(file, service_note.current_user)
		file_id = data_file["file_id"]
		file_name = data_file["file_name"]

	data = await service_note.create(note = note, file_id = file_id, service_category = service_category)
	note_dict = data["new_note"].as_dict
	note_dict["file_name"] = file_name

	if data["category"]:
		note_dict["category"] = {
			"id": data["category"].id,
			"title": data["category"].title,
			"slug": data["category"].slug
		}

	return note_dict


@router.get(
	"/file/{file_name}"
)
async def get_file_api(
	slug_project: str,
	file_name: str,
	current_user: UserInDB = Depends(get_current_user)
):
	file = await get_file(file_name, current_user)
	if not file:
		raise HTTPException(status_code = 404, detail = "File not found")

	def iterfile():
		with open(file.file_path, "rb") as file_like:
			yield from file_like

	return StreamingResponse(iterfile())
