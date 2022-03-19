from fastapi import (
	APIRouter, HTTPException, UploadFile,
	Depends
)
from fastapi import File
from fastapi.responses import StreamingResponse

from schemas import (
	NoteSchema, NoteDeleted, NoteEdit,
	NoteList, NoteCreate
)

from utils.db import (
	get_notes, get_note, deleting_note,
	editing_note, creating_note, set_file_note,
	get_file, 
)
from utils.users import get_current_user

from config import oauth2_scheme


router = APIRouter(
	prefix = "/note",
	tags = ["note"],
	responses = {404: {"description": "Not found"}},
)


@router.get(
	"/",
	response_model = NoteList,
	response_model_exclude_unset = True,
)
async def list_notes(token: str = Depends(oauth2_scheme)):
	current_user = await get_current_user(token)
	notes = await get_notes(current_user)
	return {"notes": notes}


@router.get(
	"/{note_id:int}",
	response_model = NoteSchema,
	response_model_exclude = {"id_file"}
)
async def get_note_api(
	note_id: int,
	token: str = Depends(oauth2_scheme)
) -> NoteSchema:
	current_user = await get_current_user(token)
	note = await get_note(note_id, current_user)

	if not note:
		raise HTTPException(status_code = 404, detail = "Note not found")

	return note


@router.delete("/delete")
async def delete_note(
	note: NoteDeleted,
	token: str = Depends(oauth2_scheme)
):
	current_user = await get_current_user(token)
	is_deleted_note = await deleting_note(note, current_user)

	if not is_deleted_note:
		raise HTTPException(status_code = 404, detail = "Note not found")


@router.put(
	"/edit",
	response_model = NoteEdit
)
async def edit_note(
	note: NoteEdit = Depends(),
	file: UploadFile = File(None),
	token: str = Depends(oauth2_scheme)
):
	current_user = await get_current_user(token)
	data_file = {}
	if file:
		data_file = await set_file_note(file, current_user)

	note = await editing_note(note, data_file, current_user)

	if data_file:
		note.file_name = data_file["file_name"]

	return note


@router.post(
	"/create",
	response_model = NoteSchema
)
async def create_note(
	note: NoteCreate = Depends(),
	file: UploadFile = File(None),
	token: str = Depends(oauth2_scheme)
) -> NoteSchema:
	current_user = await get_current_user(token)
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
	token: str = Depends(oauth2_scheme)
):
	current_user = await get_current_user(token)
	file = await get_file(file_name, current_user)

	if not file:
		raise HTTPException(status_code = 404, detail = "File not found")

	def iterfile():
		with open(file.file_path, "rb") as file_like:
			yield from file_like

	return StreamingResponse(iterfile())
