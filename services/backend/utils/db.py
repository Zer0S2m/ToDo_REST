import os

from typing import Union
from typing import List

from datetime import datetime

from fastapi import UploadFile

from sqlalchemy.future import select

from models import (
	Note, File, User,
	Category, Session
)

from schemas.user import (
	UserCreate, UserInDB,
)
from schemas.note import (
	NoteSchema, NoteDeleted, NoteEdit,
	NoteCreate
)
from schemas.category import (
	CategoryCreate, CategorySchema
)

from utils.common import (
	create_note_schema, delete_file_storage, check_path_media_dir,
	writing_file, check_file_is_storage, create_unique_name_file,
	create_slug_category, 
)
from utils.password import get_password_hash

from config import MEDIA_DIR


async def get_notes(
	current_user: UserInDB
) -> List[NoteSchema]:
	notes = []

	async with Session.begin() as session:
		result = await session.execute(
			select(Note).filter_by(user_id = current_user.user_id)
		)
		for note in result.scalars():
			category_slug = await get_category(current_user, category_id = note.category_id)
			if category_slug:
				category_slug = category_slug.slug
			file_name = await get_file_name(session, note.id_file)
			notes.append(create_note_schema(note, file_name, category_slug))

	return notes


async def get_note(
	note_id: int,
	current_user: UserInDB
) -> Union[None, NoteSchema]:
	async with Session.begin() as session:
		note = await session.execute(
			select(Note).filter_by(id = note_id, user_id = current_user.user_id)
		)
		note = note.scalars().first()
		if note:
			category_slug = await get_category(current_user, category_id = note.category_id)
			if category_slug:
				category_slug = category_slug.slug
			file_name = await get_file_name(session, note.id_file)
			note = create_note_schema(note, file_name, category_slug)

	return note


async def creating_note(
	note: NoteCreate,
	id_file: int,
	file_name: Union[str, bool],
	current_user: UserInDB
) -> NoteSchema:
	async with Session.begin() as session:
		category_slug = None
		new_note = Note(
			title = note.title,
			text = note.text,
			pub_date = datetime.now(),
			user_id = current_user.user_id,
			importance = note.importance
		)
		if id_file:
			new_note.id_file = id_file
		if note.category_slug:
			category = await get_category(current_user, slug = note.category_slug)
			new_note.category_id = category.id
			category_slug = category.slug

		session.add(new_note)

	return create_note_schema(new_note, file_name, category_slug)


async def deleting_note(
	note: NoteDeleted,
	current_user: UserInDB
):
	async with Session() as session:
		result = await session.execute(
			select(Note).filter_by(id = note.id, user_id = current_user.user_id)
		)
		deleted_note = result.scalars().first()
		file_name = await get_file_name(session, deleted_note.id_file)

		await delete_file_storage(file_name)

		await session.delete(deleted_note)
		await session.commit()


async def editing_note(
	note: NoteEdit,
	data_file: dict,
	current_user: UserInDB
) -> NoteEdit:
	async with Session() as session:
		note_edit = await session.execute(
			select(Note).filter_by(id = note.id, user_id = current_user.user_id)
		)
		note_edit = note_edit.scalars().first()

		if note.category_slug:
			category = await get_category(current_user, slug = note.category_slug)
			category_id = category.id
			note_edit.category_id = category_id
		else:
			note_edit.category_id = 0

		if note.importance == None:
			note_edit.importance = 0
		elif int(note.importance) != 0:
			note_edit.importance = note.importance

		if data_file:
			await delete_file_storage(note.file_name)
			await deleting_file_db(session, note.file_name)

			note_edit.id_file = data_file["id_file"]
			note.file_name = data_file["file_name"]

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


async def creating_file_note(
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

	id_file = await creating_file_note(file_path, file_name, current_user)
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
	if email:
		async with Session.begin() as session:
			user = await session.execute(
				select(User).filter_by(email = email)
			)
			user = user.scalars().first()
			if user:
				return True

	return False


async def create_category(
	category: CategoryCreate,
	current_user: UserInDB
) -> Category:
	async with Session.begin() as session:
		slug = create_slug_category(category.slug, current_user.user_id)
		new_category = Category(
			title = category.title,
			slug = slug,
			user_id = current_user.user_id
		)
		session.add(new_category)
		await session.commit()

	return new_category


async def get_categories(
	current_user: UserInDB
) -> List[CategorySchema]:
	categories = []

	async with Session.begin() as session:
		result = await session.execute(
			select(Category).filter_by(user_id = current_user.user_id)
		)
		for category in result.scalars():
			categories.append(CategorySchema(
				title = category.title,
				slug = category.slug,
			))

	return categories


async def get_notes_category(
	slug: str,
	current_user: UserInDB
) -> List[NoteSchema]:
	notes = []
	category = await get_category(current_user, slug = slug)

	async with Session.begin() as session:
		result = await session.execute(
			select(Note).filter_by(user_id = current_user.user_id, category_id = category.id)
		)
		for note in result.scalars():
			if category:
				category_slug = category.slug
			file_name = await get_file_name(session, note.id_file)
			notes.append(create_note_schema(note, file_name, category_slug))

	return notes


async def get_category(
	current_user: UserInDB,
	category_id: Union[int, None] = None,
	slug: Union[str, None] = None,
) -> Union[Category, None]:
	category = None
	async with Session.begin() as session:
		if slug:
			category = await session.execute(
				select(Category).filter_by(slug = slug, user_id = current_user.user_id)
			)
		elif category_id:
			category = await session.execute(
				select(Category).filter_by(id = category_id, user_id = current_user.user_id)
			)

	if category:
		category = category.scalars().first()
	return category


async def delete_category(
	slug: str,
	current_user: UserInDB
):
	async with Session.begin() as session:
		deleted_category = await session.execute(
			select(Category).filter_by(slug = slug, user_id = current_user.user_id)
		)
		deleted_category = deleted_category.scalars().first()
		if deleted_category:
			await session.delete(deleted_category)
			await session.commit()
