from typing import List

from fastapi import (
	APIRouter, Depends, HTTPException
)

from schemas.category import (
	CategoryCreate, CategoryDelete, CategorySchema
)
from schemas.note import NoteSchema
from schemas.user import UserInDB
from models import Category

from utils.users import get_current_user
from utils.common import (
	set_category_note, set_file_name_note, check_is_project_in_db
)
from utils.db.category import ServiceDBCategory
from utils.slug import create_slug_category


router = APIRouter(
	prefix = "/project",
	tags = ["project"],
	responses = {404: {"description": "Not found"}},
)


async def check_is_category_in_db(
	slug: str,
	service: ServiceDBCategory
):
	category = await service.fetch_one(slug = slug)
	if not category:
		raise HTTPException(status_code = 404, detail = "Category not found")


@router.get(
	"/{slug_project:str}/category",
	response_model = List[CategorySchema],
	tags = ["category"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def get_categories(
	slug_project: str,
	service: ServiceDBCategory = Depends()
) -> List[Category]:
	categories_db = await service.fetch_all(slug_project = slug_project)
	return categories_db


@router.get(
	"/{slug_project:str}/category/{slug_category:str}",
	response_model = List[NoteSchema],
	tags = ["category"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def get_category_notes(
	slug_project: str,
	slug_category: str,
	current_user: UserInDB = Depends(get_current_user),
	service: ServiceDBCategory = Depends()
) -> List[dict]:
	await check_is_category_in_db(slug_category, service)

	notes = []

	notes_db = await service.get_notes_category(slug_category)
	for note in notes_db:
		note_dict = set_category_note(note = note)
		note_dict = set_file_name_note(note = note, note_dict = note_dict)
		notes.append(note_dict)

	return notes


@router.post(
	"/{slug_project:str}/category/create",
	response_model = CategorySchema,
	tags = ["category"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def category_create(
	category: CategoryCreate,
	slug_project: str,
	current_user: UserInDB = Depends(get_current_user),
	service: ServiceDBCategory = Depends()
) -> Category:
	slug = create_slug_category(category.slug, current_user.user_id)
	category_in_db = await service.fetch_one(slug = slug)
	if category_in_db:
		raise HTTPException(status_code = 400, detail = "Category already exists")

	new_category = await service.create(category)
	return new_category


@router.delete(
	"/{slug_project:str}/category/delete",
	tags = ["category"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def category_delete(
	category: CategoryDelete,
	slug_project: str,
	current_user: UserInDB = Depends(get_current_user),
	service: ServiceDBCategory = Depends()
):
	await check_is_category_in_db(category.slug, service)
	await service.delete(category.slug)
