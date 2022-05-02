from typing import (
	List, Optional
)

from fastapi import Depends

from sqlalchemy import (
	select, or_
)
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
	Note, Category, Session,
	get_session
)

from schemas.user import UserInDB
from schemas.category import CategoryCreate
from models import Project

from utils.slug import create_slug_category
from utils.users import get_current_user


class ServiceDBCategory():
	def __init__(
		self,
		session: AsyncSession = Depends(get_session),
		current_user: UserInDB = Depends(get_current_user)
	) -> None:
		self.session = session
		self.current_user = current_user

	async def fetch_all(
		self,
		slug_project: str
	) -> List[Category]:
		result = await self.session.execute(
			select(Category, Project)
			.filter_by(user_id = self.current_user.user_id)
			.where(
				Category.project_id == Project.id, Project.slug == slug_project
			)
			.options(selectinload(Category.notes))
		)

		categories = result.scalars().all()

		return categories

	async def fetch_one(
		self,
		category_id: Optional[int] = None,
		slug: Optional[str] = None,
	) -> Optional[Category]:
		category = None
		if slug:
			category = await self.session.execute(
				select(Category)
				.filter_by(slug = slug, user_id = self.current_user.user_id)
			)
		elif category_id:
			category = await self.session.execute(
				select(Category)
				.filter_by(id = category_id, user_id = self.current_user.user_id)
			)

		if category:
			category = category.scalars().first()

		return category

	async def get_notes_category(
		self,
		slug: str,
	) -> List[Note]:
		category = await self.session.execute(
			select(Category, Note)
			.filter_by(user_id = self.current_user.user_id)
			.where(
				or_(Category.slug == slug, Note.category_id == Category.id)
			)
			.options(
				selectinload(Category.notes)
			)
		)
		category = category.scalars().first()
		return category.notes

	async def create(
		self,
		category: CategoryCreate,
	) -> Category:
		slug = create_slug_category(category.slug, self.current_user.user_id)
		new_category = Category(
			title = category.title,
			slug = slug,
			user_id = self.current_user.user_id,
			project_id = category.project_id
		)
		self.session.add(new_category)
		await self.session.commit()

		return new_category

	async def delete(
		self,
		slug: str
	) -> None:
		deleted_category = await self.session.execute(
			select(Category).filter_by(slug = slug, user_id = self.current_user.user_id)
		)
		deleted_category = deleted_category.scalars().first()
		await self.session.delete(deleted_category)
		await self.session.commit()
