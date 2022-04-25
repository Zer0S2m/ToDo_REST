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
from utils.db.category import (
	create_category_db, get_categories_db, delete_category_db,
	get_category_db, get_notes_category_db
)
from utils.slug import (
	create_slug_category
)


router = APIRouter(
	prefix = "/project",
	tags = ["project"],
	responses = {404: {"description": "Not found"}},
)


async def check_is_category_in_db(
	slug: str,
	current_user: UserInDB
):
	category = await get_category_db(current_user, slug = slug)
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
	current_user: UserInDB = Depends(get_current_user),
) -> List[Category]:
	categories_db = await get_categories_db(current_user = current_user, slug_project = slug_project)
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
) -> List[dict]:
	await check_is_category_in_db(slug_category, current_user)

	notes = []

	notes_db = await get_notes_category_db(slug_category, current_user)
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
	current_user: UserInDB = Depends(get_current_user)
) -> Category:
	slug = create_slug_category(category.slug, current_user.user_id)
	category_in_db = await get_category_db(current_user, slug = slug)
	if category_in_db:
		raise HTTPException(status_code = 400, detail = "Category already exists")

	new_category = await create_category_db(category, current_user)
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
):
	await check_is_category_in_db(category.slug, current_user)
	await delete_category_db(category.slug, current_user)
