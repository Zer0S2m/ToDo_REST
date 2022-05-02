from typing import List

from fastapi import (
	APIRouter, Depends, HTTPException
)

from schemas.user import UserInDB
from schemas.project.project import (
	ProjectCreate, ProjectDeleted, ProjectSchema,
	ProjectMain, ProjectEdit
)
from schemas.project.part import (
	PartSchema, PartCreate, PartList,
	PartDeleted, PartEdit
)
from schemas.project.comment import (
	CommentCreate, CommentSchema, CommentDeleted,
	CommentEdit
)

from utils.users import get_current_user
from utils.db.project import (
	ServiceDBProject, ServiceDBPart, ServiceDBComment
)
from utils.db.project import (
	get_project_db_for_check
)
from utils.common import (
	set_category_note, set_file_name_note, check_is_project_in_db
)
from utils.slug import (
	create_slug_project
)

from models import (
	Part, Project, Comment,
	set_count_notes_importance_levels
)


router = APIRouter(
	prefix = "/project",
	tags = ["project"],
	responses = {404: {"description": "Not found"}},
)


async def check_is_part_in_db(
	slug_part: str,
	slug_project: str,
	service: ServiceDBPart = Depends()
) -> Part:
	part_db = await service.fetch_one(slug_project, slug_part)
	if not part_db:
		raise HTTPException(status_code = 404, detail = "Part not found")
	return part_db


@router.get(
	"/",
	response_model = List[ProjectMain]
)
async def get_projects(
	service: ServiceDBProject = Depends()
) -> List[dict]:
	projects_db = await service.fetch_all()
	projects = [project.__call__() for project in projects_db]
	return projects


@router.post(
	"/create",
	response_model = ProjectSchema,
)
async def create_project(
	project: ProjectCreate,
	current_user: UserInDB = Depends(get_current_user),
	service: ServiceDBProject = Depends()
) -> dict:
	slug_project = create_slug_project(project.slug, current_user.user_id)
	is_project = await get_project_db_for_check(slug_project, current_user)
	if is_project:
		raise HTTPException(status_code = 400, detail = "Project already exists")

	new_project = await service.create(project)
	new_project = new_project.as_dict
	new_project.update({"parts": [], "comments": [], "categories": []})
	return new_project


@router.delete("/delete")
async def delete_project(
	project: ProjectDeleted,
	service: ServiceDBProject = Depends(),
):
	await service.delete(project)


@router.put(
	"/edit",
	response_model = ProjectEdit
)
async def edit_project(
	part: ProjectEdit,
	service: ServiceDBProject = Depends()
) -> Project:
	project_db = await service.edit(part)
	return project_db


@router.get(
	"/{slug_project:str}",
	response_model = ProjectSchema
)
async def get_project(
	slug_project: str,
	service: ServiceDBProject = Depends()
) -> dict:
	project_db = await service.fetch_one(slug_project)
	if not project_db:
		raise HTTPException(status_code = 404, detail = "Project not found")

	project = project_db.as_dict
	parts = []
	for part in project_db.parts:
		part_dict = part.as_dict
		part_dict.update(part.serialize_project_detail)
		parts.append(part_dict)

	project.update({
		"comments": project_db.comments,
		"parts": parts,
		"categories": project_db.categories
	})

	return project


@router.get(
	"/{slug_project:str}/part/",
	response_model = List[PartList],
	tags = ["part"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def get_parts(
	slug_project: str,
	service: ServiceDBPart = Depends()
) -> List[dict]:
	parts_db = await service.fetch_all(slug_project)
	parts = []

	for part in parts_db:
		part_dict = part.as_dict
		part_dict.update(part.serialize_project_detail)
		parts.append(part_dict)

	return parts


@router.get(
	"/{slug_project:str}/part/{slug_part:str}",
	response_model = PartSchema,
	tags = ["part"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def get_part(
	part_db: Part = Depends(check_is_part_in_db)
) -> dict:
	part = part_db.as_dict
	notes = []

	for note in part_db.notes:
		note_dict = set_category_note(note = note)
		note_dict = set_file_name_note(note = note, note_dict = note_dict)
		notes.append(note_dict)

	part.update({"notes": notes})

	return part


@router.post(
	"/{slug_project:str}/part/create",
	response_model = PartList,
	tags = ["part"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def create_part(
	part: PartCreate,
	slug_project: str,
	service: ServiceDBPart = Depends()
):
	new_part = await service.create(part)

	part = new_part.as_dict
	part.update({
		"notes": [],
		"count_notes": len([]),
		"count_notes_importance_levels": set_count_notes_importance_levels([])
	})

	return part


@router.delete(
	"/{slug_project:str}/part/delete",
	tags = ["part"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def delete_part(
	part: PartDeleted,
	slug_project: str,
	service: ServiceDBPart = Depends()
):
	await service.delete(part)


@router.put(
	"/{slug_project:str}/part/edit",
	tags = ["part"],
	response_model = PartEdit,
	dependencies = [Depends(check_is_project_in_db)],
)
async def edit_part(
	slug_project: str,
	part: PartEdit,
	service: ServiceDBPart = Depends()
) -> Part:
	part_db = await service.edit(part)
	return part_db


@router.get(
	"/{slug_project:str}/comment",
	tags = ["comment"],
	response_model = List[CommentSchema],
	dependencies = [Depends(check_is_project_in_db)]
)
async def get_comments(
	slug_project: str,
	service: ServiceDBComment = Depends()
) -> List[Comment]:
	comments = await service.fetch_all(slug_project)
	return comments


@router.post(
	"/{slug_project:str}/comment/create",
	tags = ["comment"],
	response_model = CommentSchema,
	dependencies = [Depends(check_is_project_in_db)]
)
async def create_comment(
	slug_project: str,
	comment: CommentCreate,
	service: ServiceDBComment = Depends()
) -> Comment:
	new_comment = await service.create(comment)
	return new_comment


@router.put(
	"/{slug_project:str}/comment/edit",
	tags = ["comment"],
	response_model = CommentSchema,
	dependencies = [Depends(check_is_project_in_db)]
)
async def edit_comment(
	slug_project: str,
	comment: CommentEdit,
	service: ServiceDBComment = Depends()
):
	editing_comment = await service.edit(comment)
	return editing_comment


@router.delete(
	"/{slug_project:str}/comment/delete",
	tags = ["comment"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def delete_comment(
	slug_project: str,
	comment: CommentDeleted,
	service: ServiceDBComment = Depends()
):
	await service.delete(comment)
