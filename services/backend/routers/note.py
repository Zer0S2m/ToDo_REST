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

from utils.db.note import (
	get_notes_db, get_note_db, delete_note_db,
	edit_note_db, craete_note_db, set_file_note,
	get_file, complete_note_db
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
	current_user: UserInDB
) -> Note:
	note = await get_note_db(note_id, current_user)
	if not note:
		raise HTTPException(status_code = 404, detail = "Note not found")
	return note


@router.get(
	"/",
	response_model = List[NoteSchema],
	response_model_exclude_unset = True
)
async def list_notes(
	slug_project: str,
	current_user: UserInDB = Depends(get_current_user)
) -> List[dict]:
	notes = []

	notes_db = await get_notes_db(current_user, slug_project)
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
	current_user: UserInDB = Depends(get_current_user)
) -> dict:
	note = await check_is_note_in_db(note_id, current_user)
	note_dict = set_category_note(note = note)
	note_dict = set_file_name_note(note = note, note_dict = note_dict)

	return note_dict


@router.delete("/delete")
async def delete_note(
	slug_project: str,
	note: NoteDeleted,
	current_user: UserInDB = Depends(get_current_user)
):
	await check_is_note_in_db(note.id, current_user)
	await delete_note_db(note, current_user)


@router.put(
	"/edit",
	response_model = NoteSchema
)
async def edit_note(
	slug_project: str,
	note: NoteEdit = Depends(),
	file: UploadFile = File(None),
	current_user: UserInDB = Depends(get_current_user)
)-> dict:
	await check_is_note_in_db(note.id, current_user)

	data_file = {}
	if file:
		data_file = await set_file_note(file, current_user)

	note = await edit_note_db(note, data_file, current_user)
	note_dict = note.as_dict
	note_dict = set_category_note(note = note)

	return note_dict


@router.patch(
	"/complete"
)
async def complete_note(
	slug_project: str,
	note: NoteComplete,
	current_user: UserInDB = Depends(get_current_user)
):
	await check_is_note_in_db(note.id, current_user)
	await complete_note_db(note, current_user)


@router.post(
	"/create",
	response_model = NoteSchema,
	status_code = status.HTTP_201_CREATED
)
async def create_note(
	slug_project: str,
	note: NoteCreate = Depends(),
	file: UploadFile = File(None),
	current_user: UserInDB = Depends(get_current_user)
) -> dict:
	file_id = 0
	file_name = None

	if file:
		data_file = await set_file_note(file, current_user)
		file_id = data_file["file_id"]
		file_name = data_file["file_name"]

	data = await craete_note_db(note = note, file_id = file_id, current_user = current_user)
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
