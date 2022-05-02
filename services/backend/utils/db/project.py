from typing import List

from datetime import datetime

from fastapi import Depends

from sqlalchemy import (
	select, and_
)
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
	Session, Project, Comment,
	Part, Note, get_session
)

from schemas.user import UserInDB
from schemas.project.project import (
	ProjectCreate, ProjectDeleted, ProjectEdit
)
from schemas.project.part import (
	PartCreate, PartDeleted, PartEdit
)
from schemas.project.comment import (
	CommentCreate, CommentDeleted, CommentEdit
)

from utils.users import get_current_user
from utils.slug import (
	create_slug_part, create_slug_project
)


class ServiceDBProject():
	def __init__(
		self,
		session: AsyncSession = Depends(get_session),
		current_user: UserInDB = Depends(get_current_user)
	) -> None:
		self.session = session
		self.current_user = current_user

	async def fetch_all(self) -> List[Project]:
		projects_db = await self.session.execute(
			select(Project)
			.filter_by(user_id = self.current_user.user_id)
			.options(
				selectinload(Project.parts), selectinload(Project.comments),
				selectinload(Project.categories)
			)
		)
		projects_db = projects_db.scalars().all()

		return projects_db

	async def fetch_one(
		self,
		slug: str,
	) -> Project:
		project = await self.session.execute(
			select(Project)
			.filter_by(user_id = self.current_user.user_id)
			.where(
				Project.slug == slug,
			)
			.options(
				selectinload(Project.comments),
				selectinload(Project.parts)
					.selectinload(Part.notes.and_(Note.active == True)),
				selectinload(Project.categories)
			)
		)
		project = project.scalars().first()

		return project

	async def create(
		self,
		project: ProjectCreate
	) -> Project:
		slug_project = create_slug_project(project.slug, self.current_user.user_id)

		new_project = Project(
			title = project.title,
			slug = slug_project,
			description = project.description,
			user_id = self.current_user.user_id,
			pub_date = datetime.now(),
		)
		self.session.add(new_project)
		await self.session.commit()

		return new_project

	async def edit(
		self,
		edit_project: ProjectEdit,
	):
		project = await self.session.execute(
			select(Project)
			.filter_by(user_id = self.current_user.user_id)
			.where(Project.id == edit_project.id)
		)
		project = project.scalars().first()

		for key, value in edit_project.dict(exclude = {"id"}).items():
			setattr(project, key, value)

		await self.session.commit()

		return project

	async def delete(
		self,
		project: ProjectDeleted,
	) -> Project:
		project_deleted = await self.session.execute(
			select(Project)
			.filter_by(slug = project.slug, user_id = self.current_user.user_id)
		)
		project_deleted = project_deleted.scalars().first()
		await self.session.delete(project_deleted)
		await self.session.commit()


async def get_project_db_for_check(
	slug: str,
	current_user: UserInDB
):
	async with Session.begin() as session:
		project = await session.execute(
			select(Project)
			.filter_by(user_id = current_user.user_id, slug = slug)
		)
		project = project.scalars().first()

	return project


class ServiceDBPart():
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
	) -> List[Part]:
		parts_db = await self.session.execute(
			select(Part, Project)
			.filter_by(user_id = self.current_user.user_id)
			.where(
				Project.slug == slug_project, Part.project_id == Project.id
			)
			.options(
				selectinload(Part.notes.and_(Note.active == True))
			)
		)
		parts_db = parts_db.scalars().all()

		return parts_db

	async def fetch_one(
		self,
		slug_project: str,
		slug_part: str,
	):
		part = await self.session.execute(
			select(Part, Project)
			.filter_by(user_id = self.current_user.user_id)
			.where(
				and_(
					Part.slug == slug_part,
					Part.project_id == Project.id,
					Project.slug == slug_project,
				)
			)
			.options(
				selectinload(Part.notes.and_(Note.active == True))
			)
		)
		part = part.scalars().first()

		return part

	async def create(
		self,
		part: PartCreate,
	) -> Part:
		slug_part = create_slug_part(part.slug, part.id_project)

		new_part = Part(
			title = part.title,
			slug = slug_part,
			description = part.description,
			user_id = self.current_user.user_id,
			project_id = part.id_project,
			pub_date = datetime.now(),
		)
		self.session.add(new_part)
		await self.session.commit()
		await self.session.refresh(new_part)

		return new_part

	async def delete(
		self,
		part: PartDeleted,
	):
		deleted_part = await self.session.execute(
			select(Part)
			.filter_by(user_id = self.current_user.user_id, slug = part.slug)
		)
		deleted_part = deleted_part.scalars().first()
		await self.session.delete(deleted_part)
		await self.session.commit()

	async def edit(
		self,
		edit_part: PartEdit,
	) -> Part:
		part = await self.session.execute(
			select(Part)
			.filter_by(user_id = self.current_user.user_id)
			.where(Part.id == edit_part.id)
		)
		part = part.scalars().first()

		for key, value in edit_part.dict(exclude = {"id"}).items():
			setattr(part, key, value)

		await self.session.commit()

		return part


class ServiceDBComment():
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
	) -> List[Comment]:
		comments_db = await self.session.execute(
			select(Comment, Project)
			.filter_by(user_id = self.current_user.user_id)
			.where(
				Project.slug == slug_project,
				Comment.user_id == self.current_user.user_id,
				Comment.project_id == Project.id
			)
		)
		comments_db = comments_db.scalars().all()

		return comments_db

	async def create(
		self,
		comment: CommentCreate,
	) -> Comment:
		new_comment = Comment(
			text = comment.text,
			pub_date = datetime.now(),
			user_id = self.current_user.user_id,
			project_id = comment.id_project
		)
		self.session.add(new_comment)
		await self.session.commit()

		return new_comment

	async def edit(
		self,
		comment: CommentEdit
	) -> Comment:
		editing_comment = await self.session.execute(
			select(Comment)
			.where(
				Comment.user_id == self.current_user.user_id,
				Comment.id == comment.id
			)
		)
		editing_comment = editing_comment.scalars().first()

		editing_comment.text = comment.text
		await self.session.commit()

		return editing_comment

	async def delete(
		self,
		comment: CommentDeleted
	):
		deleted_comment = await self.session.execute(
			select(Comment)
			.filter_by(
				id = comment.id,
				user_id = self.current_user.user_id
			)
		)
		deleted_comment = deleted_comment.scalars().first()
		await self.session.delete(deleted_comment)
		await self.session.commit()
