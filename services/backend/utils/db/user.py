from sqlalchemy import select

from models import User
from models import Session

from schemas.user import UserCreate

from utils.password import get_password_hash


async def create_user_db(
	user: UserCreate
) -> User:
	hash_password = get_password_hash(user.password)

	async with Session.begin() as session:
		new_user = User(
			username = user.username.strip(),
			password = hash_password
		)
		if user.email:
			new_user.email = user.email

		session.add(new_user)
		await session.commit()

	return new_user


async def get_user(
	username: str
) -> User:
	async with Session.begin() as session:
		user = await session.execute(
			select(User).filter_by(username = username)
		)
		user = user.scalars().first()

	return user


async def check_email_user_is_db(
	email: str
) -> User:
	if email:
		async with Session.begin() as session:
			user = await session.execute(
				select(User).filter_by(email = email)
			)
			user = user.scalars().first()

		return user
