from typing import List
from typing import Optional

from sqlalchemy import (
	select, or_
)
from sqlalchemy.orm import selectinload

from models import (
	Note, Category, Session,
)

from schemas.user import UserInDB
from schemas.category import CategoryCreate
from models import Project

from utils.slug import (
	create_slug_category,
)


async def create_category_db(
	category: CategoryCreate,
	current_user: UserInDB
) -> Category:
	async with Session.begin() as session:
		slug = create_slug_category(category.slug, current_user.user_id)
		new_category = Category(
			title = category.title,
			slug = slug,
			user_id = current_user.user_id,
			project_id = category.project_id
		)
		session.add(new_category)
		await session.commit()

	return new_category


async def get_categories_db(
	current_user: UserInDB,
	slug_project: str
) -> List[Category]:
	async with Session.begin() as session:
		result = await session.execute(
			select(Category, Project)
			.filter_by(user_id = current_user.user_id)
			.where(
				Category.project_id == Project.id, Project.slug == slug_project
			)
			.options(selectinload(Category.notes))
		)

		categories = result.scalars().all()

	return categories


async def get_notes_category_db(
	slug: str,
	current_user: UserInDB
) -> List[Note]:
	async with Session.begin() as session:
		category = await session.execute(
			select(Category, Note)
			.filter_by(user_id = current_user.user_id)
			.where(
				or_(Category.slug == slug, Note.category_id == Category.id)
			)
			.options(
				selectinload(Category.notes)
			)
		)
		category = category.scalars().first()

	if category:
		return category.notes
	else:
		return []


async def get_category_db(
	current_user: UserInDB,
	category_id: Optional[int] = None,
	slug: Optional[str] = None,
) -> Optional[Category]:
	category = None
	async with Session.begin() as session:
		if slug:
			category = await session.execute(
				select(Category)
				.filter_by(slug = slug, user_id = current_user.user_id)
			)
		elif category_id:
			category = await session.execute(
				select(Category)
				.filter_by(id = category_id, user_id = current_user.user_id)
			)

	if category:
		category = category.scalars().first()

	return category


async def delete_category_db(
	slug: str,
	current_user: UserInDB
):
	async with Session.begin() as session:
		deleted_category = await session.execute(
			select(Category).filter_by(slug = slug, user_id = current_user.user_id)
		)
		deleted_category = deleted_category.scalars().first()
		await session.delete(deleted_category)
		await session.commit()
