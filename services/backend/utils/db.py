import os
from typing import Union

from fastapi import UploadFile

from sqlalchemy.future import select

from models import (
	Note, File, User,
	Session
)

from schemas import (
	NoteSchema, NoteDeleted, NoteEdit,
	UserCreate, NoteCreate
)

from utils.common import (
	get_pub_date_note, delete_file_storage, check_path_media_dir,
	writing_file, check_file_is_storage, create_unique_name_file
)
from utils.users import get_password_hash

from config import MEDIA_DIR


async def get_notes():
	notes = []

	async with Session.begin() as session:
		result = await session.execute(
			select(Note)
		)
		for note in result.scalars():
			file_name = await get_file_name(session, note.id_file)
			notes.append(NoteSchema(
				titleNote = note.title,
				textNote = note.text,
				idNote = note.id,
				pubDate = get_pub_date_note(note.pub_date),
				fileName = file_name
			))

	return notes


async def get_note(
	note_id: int
) -> Union[None, NoteSchema]:
	note = None

	async with Session.begin() as session:
		result = await session.execute(
			select(Note).filter_by(id = note_id)
		)
		result = result.scalars().first()
		if result:
			file_name = await get_file_name(session, result.id_file)
			note = NoteSchema(
				idNote = result.id,
				titleNote = result.title,
				textNote = result.text,
				pubDate = get_pub_date_note(date = result.pub_date),
				fileName = file_name
			)

	return note


async def creating_note(
	note: NoteCreate,
	id_file: int,
	file_name: Union[str, bool]
) -> NoteSchema:
	async with Session.begin() as session:
		new_note = Note(
			title = note.title,
			text = note.text,
			pub_date = note.pub_date
		)
		if id_file:
			new_note.id_file = id_file

		session.add(new_note)

	return NoteSchema(
		titleNote = note.title,
		textNote = note.text,
		pubDate = get_pub_date_note(date = note.pub_date),
		idNote = new_note.id,
		fileName = file_name
	)


async def creating_file_note(
	file_path: str,
	file_name: str
) -> int:
	async with Session.begin() as session:
		new_file = File(
			file_path = file_path,
			file_name = file_name
		)
		session.add(new_file)
		await session.commit()

	return new_file.id


async def deleting_note(note: NoteDeleted):
	async with Session() as session:
		result = await session.execute(
			select(Note).filter_by(id = note.id)
		)

		deleted_note = result.scalars().first()
		file_name = await get_file_name(session, deleted_note.id_file)

		await delete_file_storage(file_name)

		await session.delete(deleted_note)
		await session.commit()


async def editing_note(
	note: NoteEdit,
	data_file: dict
):
	async with Session() as session:
		note_edit = await session.execute(
			select(Note).filter_by(id = note.id)
		)
		note_edit = note_edit.scalars().first()

		if not note.title:
			note.title = None

		if data_file:
			await delete_file_storage(note.file_name)
			await deleting_file_db(session, note.file_name)

			note_edit.id_file = data_file["id_file"]

		note_edit.title = note.title
		note_edit.text = note.text

		await session.commit()

	return note


async def deleting_file_db(
	session: Session,
	file_name: str
):
	result = await session.execute(
		select(File).filter_by(file_name = file_name)
	)
	if result:
		deleted_file = result.scalars().first()
		if deleted_file:
			await session.delete(deleted_file)
			await session.commit()


async def get_file(file_name: str) -> File:
	async with Session.begin() as session:
		file = await session.execute(
			select(File).filter_by(file_name = file_name)
		)
		file = file.scalars().first()

	return file


async def get_file_name(
	session: Session,
	id_file: int
) -> str:
	file_name = await session.execute(
		select(File).filter_by(id = id_file)
	)
	file_name = file_name.scalars().first()
	if file_name:
		file_name = file_name.file_name

	return file_name


async def set_file_note(file: UploadFile) -> dict:
	check_path_media_dir()

	if check_file_is_storage(file.filename):
		unique_name_file = create_unique_name_file(file.filename)
		file_path = os.path.join(MEDIA_DIR, unique_name_file)
		file_name = unique_name_file
	else:
		file_path = os.path.join(MEDIA_DIR, file.filename)
		file_name = file.filename

	id_file = await creating_file_note(file_path, file_name)
	await writing_file(file, file_path)

	return {
		"id_file": id_file,
		"file_name": file_name
	}


async def create_user_db(user: UserCreate) -> User:
	hash_password = get_password_hash(user.password)

	async with Session.begin() as session:
		new_user = User(
			username = user.username.strip(),
			password = hash_password
		)
		if user.email:
			new_user.email = user.email

		session.add(new_user)
		await session.commit()

	return new_user


async def get_user(
	username: str
) -> Union[User, bool]:
	async with Session.begin() as session:
		user = await session.execute(
			select(User).filter_by(username = username)
		)
		user = user.scalars().first()

		if user:
			return user
		else:
			return False


async def check_email_user_is_db(
	email: str
) -> bool:
	async with Session.begin() as session:
		user = await session.execute(
			select(User).filter_by(email = email)
		)
		user = user.scalars().first()

		if user:
			return True

	return False
