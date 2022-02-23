from fastapi import (
	APIRouter, HTTPException, UploadFile,
	Depends
)
from fastapi import File
from fastapi.responses import StreamingResponse

from schemas import (
	NoteSchema, NoteDeleted, NoteEdit,
	NoteList
)

from utils.db import (
	get_notes, get_note, deleting_note,
	editing_note, creating_note, set_file_note,
	get_file, 
)


router = APIRouter(
	prefix = "/note",
	tags = ["note"]
)


@router.get(
	"/",
	response_model = NoteList,
	response_model_exclude_unset = True,
)
async def list_notes():
	notes = await get_notes()
	return {"notes": notes}


@router.get(
	"/{note_id:int}",
	response_model = NoteSchema,
	response_model_exclude = {"id_file"}
)
async def get_note_api(
	note_id: int
) -> NoteSchema:
	note = await get_note(note_id)

	if not note:
		raise HTTPException(status_code = 404, detail = "Note not found")

	return note


@router.delete("/delete")
async def delete_note(note: NoteDeleted):
	await deleting_note(note)


@router.put(
	"/edit",
	response_model = NoteEdit
)
async def edit_note(
	note: NoteEdit = Depends(),
	file: UploadFile = File(None)
):
	data_file = {}
	if file:
		data_file = await set_file_note(file)

	note = await editing_note(note, data_file)

	if data_file:
		note.file_name = data_file["file_name"]

	return note


@router.post(
	"/create",
	response_model = NoteSchema
)
async def create_note(
	note: NoteSchema = Depends(),
	file: UploadFile = File(None)
) -> NoteSchema:
	id_file = 0
	if file:
		data_file = await set_file_note(file)

		id_file = data_file["id_file"]
		note.file_name = data_file["file_name"]

	note = await creating_note(note, id_file)
	return note


@router.get(
	"/file/{file_name}"
)
async def get_file_api(file_name: str):
	file = await get_file(file_name)

	if not file:
		raise HTTPException(status_code = 404, detail = "File not found")

	def iterfile():
		with open(file.file_path, "rb") as file_like:
			yield from file_like

	return StreamingResponse(iterfile())
