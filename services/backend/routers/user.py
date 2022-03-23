from datetime import timedelta

from fastapi import (
    Depends, APIRouter, HTTPException,
    status
)
from fastapi.security import OAuth2PasswordRequestForm

from schemas import (
    User, UserCreate, Token
)

from utils.users import (
    create_access_token, get_current_user
)
from utils.password import verify_password
from utils.db import (
    create_user_db, get_user, check_email_user_is_db
)

from config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix = "/user",
    tags = ["user"],
    responses = {404: {"description": "Not found"}},
)


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
        "accessToken": access_token,
        "tokenType": "bearer"
    }


@router.post(
    "/sign-up",
    response_model = User
)
async def create_user(user: UserCreate):
    if await check_email_user_is_db(email = user.email):
        raise HTTPException(status_code = 400, detail = {"email": "Email already registered"})
    if await get_user(username = user.username):
        raise HTTPException(status_code = 400, detail = {"username": "Username already registered"})

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
