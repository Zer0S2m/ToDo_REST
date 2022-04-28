from typing import List

from datetime import datetime

from sqlalchemy import (
	select, and_
)
from sqlalchemy.orm import selectinload

from models import (
	Session, Project, Comment,
	Part, Note
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

from utils.slug import (
	create_slug_part, create_slug_project
)


async def get_projects_db(
	current_user: UserInDB
) -> List[Project]:
	async with Session.begin() as session:
		projects_db = await session.execute(
			select(Project)
			.filter_by(user_id = current_user.user_id)
			.options(
				selectinload(Project.parts), selectinload(Project.comments),
				selectinload(Project.categories)
			)
		)
		projects_db = projects_db.scalars().all()

	return projects_db


async def get_project_db(
	slug: str,
	current_user: UserInDB
) -> Project:
	async with Session.begin() as session:
		project = await session.execute(
			select(Project)
			.filter_by(user_id = current_user.user_id)
			.where(
				Project.slug == slug,
			)
			.options(
				selectinload(Project.comments),
				selectinload(Project.parts).selectinload(Part.notes.and_(Note.active == True)),
				selectinload(Project.categories)
			)
		)
		project = project.scalars().first()

	return project


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


async def create_project_db(
	project: ProjectCreate,
	current_user: UserInDB
) -> Project:
	slug_project = create_slug_project(project.slug, current_user.user_id)

	async with Session.begin() as session:
		new_project = Project(
			title = project.title,
			slug = slug_project,
			description = project.description,
			user_id = current_user.user_id,
			pub_date = datetime.now(),
		)
		session.add(new_project)

	return new_project


async def delete_project_db(
	project: ProjectDeleted,
	current_user: UserInDB
):
	async with Session.begin() as session:
		project_deleted = await session.execute(
			select(Project)
			.filter_by(slug = project.slug, user_id = current_user.user_id)
		)
		project_deleted = project_deleted.scalars().first()
		await session.delete(project_deleted)
		await session.commit()


async def edit_project_db(
	edit_project: ProjectEdit,
	current_user: UserInDB
) -> Project:
	async with Session.begin() as session:
		project = await session.execute(
			select(Project)
			.filter_by(user_id = current_user.user_id)
			.where(Project.id == edit_project.id)
		)
		project = project.scalars().first()

		for key, value in edit_project.dict(exclude = {"id"}).items():
			setattr(project, key, value)

		await session.commit()

	return project


async def get_parts_db(
	slug_category: str,
	current_user: UserInDB,
) -> List[Part]:
	async with Session.begin() as session:
		parts_db = await session.execute(
			select(Part, Project)
			.filter_by(user_id = current_user.user_id)
			.where(
				Project.slug == slug_category, Part.project_id == Project.id
			)
			.options(
				selectinload(Part.notes.and_(Note.active == True))
			)
		)
		parts_db = parts_db.scalars().all()

	return parts_db


async def get_part_db(
	slug_project: str,
	slug_part: str,
	current_user: UserInDB,
) -> Part:
	async with Session.begin() as session:
		part = await session.execute(
			select(Part, Project)
			.filter_by(user_id = current_user.user_id)
			.where(
				and_(
					Part.slug == slug_part, Part.project_id == Project.id, Project.slug == slug_project,
				)
			)
			.options(
				selectinload(Part.notes.and_(Note.active == True))
			)
		)
		part = part.scalars().first()

	return part


async def create_part_db(
	part: PartCreate,
	current_user: UserInDB
) -> Part:
	slug_part = create_slug_part(part.slug, part.id_project)

	async with Session.begin() as session:
		new_part = Part(
			title = part.title,
			slug = slug_part,
			description = part.description,
			user_id = current_user.user_id,
			project_id = part.id_project,
			pub_date = datetime.now(),
		)
		session.add(new_part)

	return new_part


async def delete_part_db(
	part: PartDeleted,
	current_user: UserInDB
):
	async with Session.begin() as session:
		deleted_part = await session.execute(
			select(Part)
			.filter_by(user_id = current_user.user_id, slug = part.slug)
		)
		deleted_part = deleted_part.scalars().first()
		await session.delete(deleted_part)
		await session.commit()


async def edit_part_db(
	edit_part: PartEdit,
	current_user: UserInDB
) -> Part:
	async with Session.begin() as session:
		part = await session.execute(
			select(Part)
			.filter_by(user_id = current_user.user_id)
			.where(Part.id == edit_part.id)
		)
		part = part.scalars().first()

		for key, value in edit_part.dict(exclude = {"id"}).items():
			setattr(part, key, value)

		await session.commit()

	return part


async def get_comments_db(
	slug_project: str,
	current_user: UserInDB
) -> List[Comment]:
	async with Session.begin() as session:
		comments_db = await session.execute(
			select(Comment, Project)
			.filter_by(user_id = current_user.user_id)
			.where(
				Project.slug == slug_project, Comment.user_id == current_user.user_id,
				Comment.project_id == Project.id
			)
		)
		comments_db = comments_db.scalars().all()

	return comments_db


async def create_comment_db(
	comment: CommentCreate,
	current_user: UserInDB
) -> Comment:
	async with Session.begin() as session:
		new_comment = Comment(
			text = comment.text,
			pub_date = datetime.now(),
			user_id = current_user.user_id,
			project_id = comment.id_project
		)
		session.add(new_comment)

	return new_comment


async def edit_comment_db(
	comment: CommentEdit,
	current_user: UserInDB
) -> Comment:
	async with Session.begin() as session:
		editing_comment = await session.execute(
			select(Comment)
			.where(Comment.user_id == current_user.user_id, Comment.id == comment.id)
		)
		editing_comment = editing_comment.scalars().first()

		editing_comment.text = comment.text
		await session.commit()

	return editing_comment


async def delete_comment_db(
	comment: CommentDeleted,
	current_user: UserInDB
):
	async with Session.begin() as session:
		deleted_comment = await session.execute(
			select(Comment)
			.filter_by(id = comment.id, user_id = current_user.user_id)
		)
		deleted_comment = deleted_comment.scalars().first()
		await session.delete(deleted_comment)
		await session.commit()
