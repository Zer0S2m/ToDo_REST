from typing import List

from fastapi import (
	APIRouter, Depends, HTTPException
)

from schemas.user import UserInDB
from schemas.project.project import (
	ProjectCreate, ProjectDeleted, ProjectSchema,
	ProjectMain
)
from schemas.project.part import (
	PartSchema, PartCreate, PartList,
	PartDeleted
)
from schemas.project.comment import (
	CommentCreate, CommentSchema, CommentDeleted,
	CommentEdit
)

from utils.users import get_current_user
from utils.db.project import (
	create_project_db, get_projects_db, get_project_db,
	delete_project_db, create_part_db, get_parts_db,
	get_part_db, delete_part_db, get_comments_db,
	delete_comment_db, create_comment_db, edit_comment_db,
	get_project_db_for_check
)
from utils.common import (
	set_category_note, set_file_name_note, set_count_notes_importance_levels,
	check_is_project_in_db,
)
from utils.slug import (
	create_slug_project
)

from models import Part


router = APIRouter(
	prefix = "/project",
	tags = ["project"],
	responses = {404: {"description": "Not found"}},
)


async def check_is_part_in_db(
	current_user: UserInDB,
	slug_part: str,
	slug_project: str
) -> Part:
	part_db = await get_part_db(slug_project, slug_part, current_user)
	if not part_db:
		raise HTTPException(status_code = 404, detail = "Part not found")
	return part_db


@router.get(
	"/",
	response_model = List[ProjectMain]
)
async def get_projects(
	current_user: UserInDB = Depends(get_current_user),
) -> List[dict]:
	projects = []

	projects_db = await get_projects_db(current_user)
	for project in projects_db:
		parts = [part.serialize_project_main for part in project.parts]
		dict_project = project.as_dict
		dict_project.update({
			"parts": parts, "comments": project.comments, "categories": project.categories
		})
		projects.append(dict_project)

	return projects


@router.post(
	"/create",
	response_model = ProjectSchema,
)
async def create_project(
	project: ProjectCreate,
	current_user: UserInDB = Depends(get_current_user)
):
	slug_project = create_slug_project(project.slug, current_user.user_id)
	is_project = await get_project_db_for_check(slug_project, current_user)
	if is_project:
		raise HTTPException(status_code = 400, detail = "Project already exists")

	new_project = await create_project_db(project, current_user)
	new_project = new_project.as_dict
	new_project.update({"parts": [], "comments": [], "categories": []})
	return new_project


@router.delete("/delete")
async def delete_project(
	project: ProjectDeleted,
	current_user: UserInDB = Depends(get_current_user)
):
	await delete_project_db(project, current_user)


@router.get(
	"/{slug_project:str}",
	response_model = ProjectSchema
)
async def get_project(
	slug_project: str,
	current_user: UserInDB = Depends(get_current_user)
) -> dict:
	project_db = await get_project_db(slug_project, current_user)
	if not project_db:
		raise HTTPException(status_code = 404, detail = "Project not found")

	project = project_db.as_dict
	parts = []
	for part in project_db.parts:
		part_dict = part.as_dict
		part_dict.update({
			"count_notes": len(part.notes),
			"count_notes_importance_levels": set_count_notes_importance_levels(part.notes)
		})
		parts.append(part_dict)

	project.update({
		"comments": project_db.comments,
		"parts": parts,
		"categories": project_db.categories
	})

	return project


@router.post(
	"/{slug_project:str}/part/create",
	response_model = PartList,
	tags = ["part"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def create_part(
	part: PartCreate,
	slug_project: str,
	current_user: UserInDB = Depends(get_current_user)
):
	new_part = await create_part_db(part, current_user)
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
	current_user: UserInDB = Depends(get_current_user)
):
	await delete_part_db(part, current_user)


@router.get(
	"/{slug_project:str}/part/",
	response_model = List[PartList],
	tags = ["part"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def get_parts(
	slug_project: str,
	current_user: UserInDB = Depends(get_current_user),
):
	parts_db = await get_parts_db(slug_project, current_user)
	parts = []

	for part in parts_db:
		part_dict = part.as_dict
		part_dict.update({"count_notes": len(part.notes)})
		part_dict.update({"count_notes_importance_levels": set_count_notes_importance_levels(part.notes)})
		parts.append(part_dict)

	return parts


@router.get(
	"/{slug_project:str}/part/{slug_part:str}",
	response_model = PartSchema,
	tags = ["part"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def get_part(
	slug_project: str,
	slug_part: str,
	current_user: UserInDB = Depends(get_current_user)
) -> dict:
	part_db = await check_is_part_in_db(current_user, slug_part, slug_project)

	part = part_db.as_dict
	notes = []

	for note in part_db.notes:
		note_dict = set_category_note(note = note)
		note_dict = set_file_name_note(note = note, note_dict = note_dict)
		notes.append(note_dict)

	part.update({"notes": notes})

	return part


@router.get(
	"/{slug_project:str}/comment",
	tags = ["comment"],
	response_model = List[CommentSchema],
	dependencies = [Depends(check_is_project_in_db)]
)
async def get_comments(
	slug_project: str,
	current_user: UserInDB = Depends(get_current_user)
):
	comments = await get_comments_db(slug_project, current_user)
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
	current_user: UserInDB = Depends(get_current_user)
):
	new_comment = await create_comment_db(comment, current_user)
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
	current_user: UserInDB = Depends(get_current_user)
):
	editing_comment = await edit_comment_db(comment, current_user)
	return editing_comment


@router.delete(
	"/{slug_project:str}/comment/delete",
	tags = ["comment"],
	dependencies = [Depends(check_is_project_in_db)]
)
async def delete_comment(
	slug_project: str,
	comment: CommentDeleted,
	current_user: UserInDB = Depends(get_current_user)
):
	await delete_comment_db(comment, current_user)
