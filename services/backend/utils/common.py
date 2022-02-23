import os
import time
from datetime import datetime

import aiofiles

from fastapi import UploadFile

from config import MEDIA_DIR


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


def get_pub_date_note(date: datetime) -> str:
	return f'{date.strftime("%d.%m.%Y")} {date.strftime("%H:%M")}'
