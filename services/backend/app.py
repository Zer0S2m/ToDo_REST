from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import note
from routers import user


app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins = ["http://localhost:8080"],
	allow_credentials = True,
	allow_methods = ["*"],
	allow_headers = ["*"],
)

app.include_router(note.router)
app.include_router(user.router)
