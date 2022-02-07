from datetime import datetime

from fastapi import FastAPI
from fastapi import HTTPException

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.future import select

from models import Note
from models import Session

from schemas import NoteSchema
from schemas import NoteDeleted


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:8080"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.get("/")
async def index():
    async with Session() as session:
        notes_json = {}
        notes = await session.execute(select(Note))

        for note in notes.scalars():
            pub_date_note = get_pub_date_note(date = note.pub_date)

            notes_json[str(note.id)] = NoteSchema()

            notes_json[str(note.id)].title = note.title
            notes_json[str(note.id)].text = note.text
            notes_json[str(note.id)].pub_date = pub_date_note
            notes_json[str(note.id)].id = note.id

    return notes_json


@app.post("/note/create")
async def create_note(note: NoteSchema):
    async with Session.begin() as session:
        new_note = Note(
            title = note.title,
            text = note.text,
            pub_date = note.pub_date
        )

        session.add(new_note)

    note.id = new_note.id

    return note


@app.post("/note/delete")
async def delete_note(note: NoteDeleted):
    async with Session() as session:
        result = await session.execute(
            select(Note).filter_by(id = note.note_id)
        )

        deleted_note = result.scalars().first()

        await session.delete(deleted_note)
        await session.commit()


@app.get("/note/{note_id:int}")
async def get_note(note_id: int):
    async with Session() as session:
        note = False

        result = await session.execute(
            select(Note).filter_by(id = note_id)
        )

        for note_res in result.scalars():
            pub_date_note = get_pub_date_note(date = note_res.pub_date)

            note = NoteSchema()

            note.pub_date = pub_date_note
            note.title = note_res.title
            note.text = note_res.text

    if not note:
        return HTTPException(status_code = 404, detail = "Note not found")

    return note


def get_pub_date_note(date: datetime) -> str:
	return f'{date.strftime("%d.%m.%Y")} {date.strftime("%H:%M")}'
