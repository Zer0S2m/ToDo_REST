import os
import time
from typing import (
	Dict, List, Optional
)

import aiofiles

from fastapi import (
	Depends, UploadFile, HTTPException,
	Request
)

from config import MEDIA_DIR

from schemas.user import UserInDB

from utils.users import get_current_user
from utils.db.project import get_project_db_for_check

from models import (
	Note, Project
)


def check_path_media_dir():
	if not os.path.isdir(MEDIA_DIR):
		os.mkdir(MEDIA_DIR)


def check_file_is_storage(file_name: str) -> bool:
	if os.path.isfile(f"{MEDIA_DIR}\\{file_name}"):
		return True

	return False


def create_unique_name_file(file_name: str) -> str:
	split_file_name = file_name.split(".")
	_time = str(time.time()).split(".")[0]
	split_file_name[0] = f"{split_file_name[0]}-{_time}"

	return ".".join(split_file_name)


async def delete_file_storage(file_name: str):
	if check_file_is_storage(file_name):
		path = os.path.join(MEDIA_DIR, file_name)
		os.remove(path)


async def writing_file(
	file: UploadFile,
	file_path: str
):
	async with aiofiles.open(file_path, 'wb') as f:
		contents = await file.read()
		await f.write(contents)


def set_category_note(
	note: Note,
	note_dict: Optional[dict] = None,
) -> dict:
	if not note_dict:
		note_dict = note.as_dict

	note_dict["category"] = {
		"id": None,
		"slug": None,
		"title": None
	}
	note_dict["category"]["slug"] = note.category.slug if note.category else None
	note_dict["category"]["title"] = note.category.title if note.category else None
	note_dict["category"]["id"] = note.category.id if note.category else None

	return note_dict


def set_file_name_note(
	note: Note,
	note_dict: dict = None,
) -> dict:
	if not note_dict:
		note_dict = note.as_dict

	note_dict["file_name"] = note.file.file_name if note.file else None

	return note_dict


def set_count_notes_importance_levels(
	notes: List[Note]
) -> Dict[int, int]:
	count_levels = {
		0: 0,
		1: 0,
		2: 0,
		3: 0,
	}

	for note in notes:
		count_levels[note.importance] += 1

	return count_levels


async def check_is_project_in_db(
	request: Request,
	current_user: UserInDB = Depends(get_current_user)
) -> Project:
	project = await get_project_db_for_check(request.path_params["slug_project"], current_user)
	if not project:
		raise HTTPException(status_code = 404, detail = "Project not found")
	return project
