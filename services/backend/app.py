from datetime import datetime

from fastapi import FastAPI
from fastapi import HTTPException

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.future import select

from models import Note
from models import Session

from schemas import NoteSchema


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

            notes_json[str(note.id)] = {
                "title": note.title,
                "text": note.text,
                "pub_date": pub_date_note
            }

    return notes_json


@app.post("/note/create/", response_model = NoteSchema)
async def create_note(note: NoteSchema):
    async with Session.begin() as session:
        new_note = Note(
            title = note.title,
            text = note.text,
            pub_date = note.pub_date
        )

        session.add(new_note)

    return note


@app.get("/note/{note_id:int}/")
async def get_note(note_id: int):
    async with Session() as session:
        note = False

        result = await session.execute(
            select(Note).filter_by(id = note_id)
        )

        for note in result.scalars():
            pub_date_note = get_pub_date_note(date = note.pub_date)

            note = {
                "title": note.title,
                "text": note.text,
                "pub_date": pub_date_note,
            }

    if not note:
        return HTTPException(status_code = 404, detail = "Note not found")

    return note


def get_pub_date_note(date: datetime) -> str:
	return f'{date.strftime("%d.%m.%Y")} {date.strftime("%H:%M")}'
