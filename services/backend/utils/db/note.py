import os

from typing import (
	Optional, Dict, List,
	Union
)

from datetime import datetime

from fastapi import (
	UploadFile, Depends
)

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
	Note, File, Session,
	Project, Category, get_session
)

from schemas.user import UserInDB
from schemas.note import (
	NoteCreate, NoteDeleted, NoteEdit,
	NoteComplete
)

from utils.common import (
	create_unique_name_file, delete_file_storage, check_path_media_dir,
	writing_file, check_file_is_storage,
)
from utils.users import get_current_user

from .category import ServiceDBCategory

from config import MEDIA_DIR


class ServiceDBNote():
	def __init__(
		self,
		session: AsyncSession = Depends(get_session),
		current_user: UserInDB = Depends(get_current_user)
	) -> None:
		self.session = session
		self.current_user = current_user

	async def fetch_all(
		self,
		slug_project: str
	) -> List[Note]:
		notes = await self.session.execute(
			select(Note, Project)
			.filter_by(user_id = self.current_user.user_id)
			.where(
				Note.active == True,
				Project.slug == slug_project,
				Project.id == Note.project_id
			)
			.order_by(Note.pub_date.desc())
			.options(
				selectinload(Note.file), selectinload(Note.category)
			)
		)
		notes = notes.scalars().all()

		return notes

	async def fetch_one(
		self,
		note_id: int
	) -> Note:
		note = await self.session.execute(
			select(Note)
			.filter_by(user_id = self.current_user.user_id)
			.where(
				Note.id == note_id, Note.active == True
			)
			.options(selectinload(Note.file), selectinload(Note.category))
		)
		note = note.scalars().first()

		return note

	async def create(
		self,
		note: NoteCreate,
		file_id: int,
		service_category: ServiceDBCategory
	) -> Dict[str, Union[Optional[Category], Note]]:
		category = None
		new_note = Note(
			title = note.title,
			text = note.text,
			pub_date = datetime.now(),
			user_id = self.current_user.user_id,
			importance = note.importance,
			part_id = note.part_id,
			project_id = note.project_id,
		)
		if file_id:
			new_note.file_id = file_id
		if note.category_id:
			category = await service_category.fetch_one(category_id = note.category_id)
			new_note.category_id = note.category_id

		self.session.add(new_note)
		await self.session.commit()

		return {
			"new_note": new_note,
			"category": category
		}

	async def delete(
		self,
		note: NoteDeleted,
	) -> None:
		result = await self.session.execute(
			select(Note)
			.filter_by(id = note.id, user_id = self.current_user.user_id)
			.options(selectinload(Note.file))
		)
		deleted_note = result.scalars().first()

		if deleted_note.file:
			file_name = deleted_note.file.file_name
			await delete_file_storage(file_name)

		await self.session.delete(deleted_note)
		await self.session.commit()

	async def complete(
		self,
		note: NoteComplete
	) -> None:
		completed_note = await self.session.execute(
			select(Note)
			.filter_by(user_id = self.current_user.user_id)
			.where(
				Note.id == note.id
			)
		)
		completed_note = completed_note.scalars().first()
		completed_note.active = False

		await self.session.commit()

	async def edit(
		self,
		note: NoteEdit,
		data_file: dict,
	) -> Note:
		note_edit = await self.session.execute(
			select(Note)
			.filter_by(id = note.id, user_id = self.current_user.user_id)
		)
		note_edit = note_edit.scalars().first()

		if note.category_id:
			note_edit.category_id = note.category_id
		else:
			note_edit.category_id = 0

		if data_file:
			await delete_file_storage(note.file_name)
			await deleting_file_db(self.session, note.file_name)

			note_edit.file_id = data_file["file_id"]
			note.file_name = data_file["file_name"]

		note_edit.importance = note.importance
		note_edit.title = note.title
		note_edit.text = note.text
		note.pub_date = note_edit.pub_date

		await self.session.commit()
		await self.session.refresh(note_edit)

		return note_edit


async def deleting_file_db(
	session: Session,
	file_name: str
):
	file = await session.execute(
		select(File).filter_by(file_name = file_name)
	)
	file = file.scalars().first()
	if file:
		await session.delete(file)
		await session.commit()


async def get_file(
	file_name: str,
	current_user: UserInDB
) -> File:
	async with Session.begin() as session:
		file = await session.execute(
			select(File).filter_by(file_name = file_name, user_id = current_user.user_id)
		)
		file = file.scalars().first()

	return file


async def create_file_note_db(
	file_path: str,
	file_name: str,
	current_user: UserInDB
) -> int:
	async with Session.begin() as session:
		new_file = File(
			file_path = file_path,
			file_name = file_name,
			user_id = current_user.user_id
		)
		session.add(new_file)
		await session.commit()

	return new_file.id


async def set_file_note(
	file: UploadFile,
	current_user: UserInDB
) -> dict:
	check_path_media_dir()

	if check_file_is_storage(file.filename):
		unique_name_file = create_unique_name_file(file.filename)
		file_path = os.path.join(MEDIA_DIR, unique_name_file)
		file_name = unique_name_file
	else:
		file_path = os.path.join(MEDIA_DIR, file.filename)
		file_name = file.filename

	file_id = await create_file_note_db(file_path, file_name, current_user)
	await writing_file(file, file_path)

	return {
		"file_id": file_id,
		"file_name": file_name
	}
