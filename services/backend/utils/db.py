from typing import Union

from sqlalchemy.future import select

from models import (
	Note, File, Session
)

from schemas import (
	NoteSchema, NoteDeleted, NoteEdit
)

from utils.common import get_pub_date_note


async def get_notes():
	notes = []

	async with Session.begin() as session:
		result = await session.execute(
			select(Note)
		)
		for note in result.scalars():
			file_name = await get_file_name(session, note.file_id)
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
			file_name = await get_file_name(session, result.file_id)
			note = NoteSchema(
				idNote = result.id,
				titleNote = result.title,
				textNote = result.text,
				pubDate = get_pub_date_note(date = result.pub_date),
				fileName = file_name
			)

	return note


async def creating_note(note: NoteSchema) -> NoteSchema:
	async with Session.begin() as session:
		new_note = Note(
			title = note.title,
			text = note.text,
			pub_date = note.pub_date
		)
		file_name = None
		if note.id_file:
			new_note.file_id = note.id_file
			file_name = await get_file_name(session, note.id_file)

		session.add(new_note)

	note.id = new_note.id
	note.pub_date = get_pub_date_note(date = note.pub_date)
	note.file_name = file_name

	return note


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

		await session.delete(deleted_note)
		await session.commit()


async def editing_note(note: NoteEdit):
	async with Session() as session:
		note_edit = await session.execute(
			select(Note).filter_by(id = note.id)
		)
		note_edit = note_edit.scalars().first()

		if not note.title:
			note.title = None

		note_edit.title = note.title
		note_edit.text = note.text

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
	file_id: int
) -> str:
	file_name = await session.execute(
        select(File).filter_by(id=file_id)
    )
	file_name = file_name.scalars().first()
	if file_name:
		file_name = file_name.file_name

	return file_name
