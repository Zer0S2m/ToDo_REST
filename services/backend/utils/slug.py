def create_slug_project(
	slug: str,
	user_id: int
) -> str:
	slug_split = slug.strip().split(" ")
	return f"{'_'.join(slug_split)}_{user_id}"


def create_slug_part(
	slug: str,
	project_id: int
) -> str:
	slug_split = slug.strip().split(" ")
	return f"{'_'.join(slug_split)}_{project_id}"


def create_slug_category(
	slug: str,
	user_id: int
) -> str:
	slug_split = slug.strip().split(" ")
	return f"{'_'.join(slug_split)}_{user_id}"
