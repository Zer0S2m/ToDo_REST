from typing import Optional

from datetime import timedelta
from datetime import datetime

from jose import jwt
from jose import JWTError

from fastapi import (
	Depends, status, HTTPException
)

from schemas.user import (
	UserInDB, TokenData
)

from config import (
	SECRET_KEY, ALGORITHM, oauth2_scheme
)

from utils.db.user import get_user


def create_access_token(
	data: dict,
	expires_delta: Optional[timedelta] = None
):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes = 15)

	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
	return encoded_jwt


async def get_current_user(
	token: str = Depends(oauth2_scheme)
) -> UserInDB:
	credentials_exception = HTTPException(
		status_code = status.HTTP_401_UNAUTHORIZED,
		detail = "Could not validate credentials",
		headers = {"WWW-Authenticate": "Bearer"},
	)

	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception

		token_data = TokenData(username = username)
	except JWTError:
		raise credentials_exception

	user = await get_user(username = token_data.username)
	user = UserInDB(
		username = user.username,
		password = user.password,
		email = user.email,
		user_id = user.id
	)

	if user is None:
		raise credentials_exception
	return user
