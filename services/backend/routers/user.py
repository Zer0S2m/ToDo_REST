from datetime import timedelta

from fastapi import (
    Depends, APIRouter, HTTPException,
    status
)
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from jose import JWTError
from jose import jwt

from schemas import (
    User, UserInDB, UserCreate,
    Token, TokenData
)

from utils.users import create_access_token
from utils.users import verify_password
from utils.db import create_user_db
from utils.db import get_user

from config import (
    SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
)


router = APIRouter(
    prefix = "/user",
    tags = ["users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "user/auth")


async def authenticate_user(
    username: str,
    password: str
):
    user = await get_user(username = username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
        email = user.email
    )

    if user is None:
        raise credentials_exception
    return user


@router.post(
    "/auth",
    response_model = Token
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.username},
        expires_delta = access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post(
    "/sign-up",
    response_model = User
)
async def create_user(user: UserCreate):
    new_user = await create_user_db(user)
    return {
        "username": new_user.username,
        "email": new_user.email
    }


@router.get(
    "/me/",
    response_model = User
)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
