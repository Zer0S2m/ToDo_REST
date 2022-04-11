import os

from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer


BD_NAME = "db_todo"
LIMIT_NOTE_TITLE = 255
LIMIT_NOTE_TEXT = 1000
LIMIT_CATEGORY_TITLE = 50
LIMIT_CATEGORY_SLUG = 50
LIMIT_USERNAME = 50

BASEDIR = os.getcwd()
MEDIA = "media"
MEDIA_DIR = os.path.join(os.path.join(BASEDIR, MEDIA))

SECRET_KEY = "$3m=lf6hmv080jqoia=j5ke+i$m&1())-#kl^-+9h%(_m^w&c9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "user/auth")
