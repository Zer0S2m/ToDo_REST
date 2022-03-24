from fastapi import (
	APIRouter, HTTPException, UploadFile,
	Depends, File
)
from fastapi.responses import StreamingResponse

from schemas.user import UserInDB
from schemas.note import (
	NoteSchema, NoteDeleted, NoteEdit,
	NoteList, NoteCreate, 
)

from models import Note

from utils.db import (
	get_notes, get_note, deleting_note,
	editing_note, creating_note, set_file_note,
	get_file, 
)
from utils.users import get_current_user


router = APIRouter(
	prefix = "/note",
	tags = ["note"],
	responses = {404: {"description": "Not found"}},
)


async def check_is_note_in_db(
	note_id: int,
	current_user: UserInDB
) -> Note:
	note = await get_note(note_id, current_user)
	if not note:
		raise HTTPException(status_code = 404, detail = "Note not found")
	return note


@router.get(
	"/",
	response_model = NoteList,
	response_model_exclude_unset = True,
)
async def list_notes(current_user: UserInDB = Depends(get_current_user)):
	notes = await get_notes(current_user)
	return {"notes": notes}


@router.get(
	"/{note_id:int}",
	response_model = NoteSchema,
	response_model_exclude = {"id_file"}
)
async def get_note_api(
	note_id: int,
	current_user: UserInDB = Depends(get_current_user)
) -> NoteSchema:
	note = await check_is_note_in_db(note_id, current_user)
	return note


@router.delete("/delete")
async def delete_note(
	note: NoteDeleted,
	current_user: UserInDB = Depends(get_current_user)
):
	await check_is_note_in_db(note.id, current_user)
	await deleting_note(note, current_user)


@router.put(
	"/edit",
	response_model = NoteEdit
)
async def edit_note(
	note: NoteEdit = Depends(),
	file: UploadFile = File(None),
	current_user: UserInDB = Depends(get_current_user)
):
	await check_is_note_in_db(note.id, current_user)

	data_file = {}
	if file:
		data_file = await set_file_note(file, current_user)

	note = await editing_note(note, data_file, current_user)
	return note


@router.post(
	"/create",
	response_model = NoteSchema
)
async def create_note(
	note: NoteCreate = Depends(),
	file: UploadFile = File(None),
	current_user: UserInDB = Depends(get_current_user)
) -> NoteSchema:
	id_file = 0
	file_name = False

	if file:
		data_file = await set_file_note(file, current_user)
		id_file = data_file["id_file"]
		file_name = data_file["file_name"]

	note = await creating_note(note, id_file, file_name, current_user)
	return note


@router.get(
	"/file/{file_name}"
)
async def get_file_api(
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
