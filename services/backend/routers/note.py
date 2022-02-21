import os

from fastapi import (
	APIRouter, HTTPException, UploadFile,
)
from fastapi import File
from fastapi.responses import StreamingResponse

from schemas import (
	NoteSchema, NoteDeleted, NoteEdit,
	FileCreate
)
from config import MEDIA_DIR

from utils.common import (
	check_path_media_dir, writing_file, check_file_is_storage,
	create_unique_name_file
)
from utils.db import (
	get_notes, get_note, deleting_note,
	editing_note, creating_note, creating_file_note,
	get_file
)


router = APIRouter(
	prefix = "/note",
	tags = ["note"]
)


@router.get("/")
async def list_notes():
	notes = await get_notes()
	return notes


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


@router.put("/edit")
async def edit_note(
	note: NoteEdit
):
	await editing_note(note)


@router.post(
	"/create",
	response_model = NoteSchema,
	response_model_exclude = {"id_file"}
)
async def create_note(
	note: NoteSchema
) -> NoteSchema:
	note = await creating_note(note)
	return note


@router.post(
	"/create_file",
	response_model = FileCreate
)
async def create_file(
	file: UploadFile = File(None)
) -> FileCreate:
	if file:
		check_path_media_dir()

		if check_file_is_storage(file.filename):
			unique_name_file = create_unique_name_file(file.filename)
			file_path = os.path.join(MEDIA_DIR, unique_name_file)
			file_name = unique_name_file
		else:
			file_path = os.path.join(MEDIA_DIR, file.filename)
			file_name = file.filename

		file_id = await creating_file_note(file_path, file_name)
		await writing_file(file, file_path)

		return FileCreate(
			idFile = file_id,
			fileName = file_name
		)

	return FileCreate(
		idFile = None,
		fileName = None
	)


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
