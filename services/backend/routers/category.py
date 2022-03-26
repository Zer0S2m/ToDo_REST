from fastapi import (
    APIRouter, Depends, HTTPException
)

from schemas.category import (
    CategoryCreate, CategoryList, CategoryDelete,
    CategorySchema
)
from schemas.note import NoteList
from schemas.user import UserInDB

from utils.users import get_current_user
from utils.common import create_slug_category
from utils.db import (
    create_category, get_categories, delete_category,
    get_category, get_notes_category
)


router = APIRouter(
	prefix = "/category",
	tags = ["category"],
	responses = {404: {"description": "Not found"}},
)


async def check_is_category_in_db(
    slug: str,
    current_user: UserInDB
):
    category = await get_category(current_user, slug = slug)
    if not category:
        raise HTTPException(status_code = 404, detail = "Category not found")


@router.get(
    "/",
    response_model = CategoryList
)
async def category_list(current_user: UserInDB = Depends(get_current_user)):
    categories = await get_categories(current_user)
    return {"categories": categories}


@router.get(
    "/{slug:str}",
    response_model = NoteList
)
async def get_category_notes(
    slug: str,
    current_user: UserInDB = Depends(get_current_user),
):
    await check_is_category_in_db(slug, current_user)

    notes = await get_notes_category(slug, current_user)
    return {"notes": notes}


@router.post(
    "/create",
    response_model = CategorySchema
)
async def category_create(
    category: CategoryCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    slug = create_slug_category(category.slug, current_user.user_id)
    category_in_db = await get_category(current_user, slug = slug)
    if category_in_db:
        raise HTTPException(status_code = 400, detail = "Category already exists")

    new_category = await create_category(category, current_user)
    return {
        "title": new_category.title,
        "slug": new_category.slug,
    }


@router.delete(
    "/delete"
)
async def category_delete(
    category: CategoryDelete,
    current_user: UserInDB = Depends(get_current_user)
):
    await check_is_category_in_db(category.slug, current_user)
    await delete_category(category.slug, current_user)
