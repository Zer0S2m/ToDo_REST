from sqlalchemy import (
	Column, Integer, String,
	DateTime, Text, ForeignKey
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.ext.declarative import declarative_base

from config import (
    BD_NAME, LIMIT_NOTE_TITLE, LIMIT_NOTE_TEXT,
    LIMIT_CATEGORY_TITLE, LIMIT_CATEGORY_SLUG
)


engine = create_async_engine(f"sqlite+aiosqlite:///{BD_NAME}.db")
Session = sessionmaker(
    engine, expire_on_commit = False, class_ = AsyncSession
)
Base = declarative_base()


class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key = True, unique = True)
    title = Column(String(LIMIT_NOTE_TITLE), default = False)
    text = Column(Text(LIMIT_NOTE_TEXT), nullable = False)
    pub_date = Column(DateTime)
    importance = Column(Integer, default = 0)
    file_id = Column(Integer, ForeignKey('file.id', ondelete = "CASCADE"), default = False)
    file = relationship("File", backref = "note_file", cascade = "all, delete")
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id', ondelete = "CASCADE"), nullable = True, default = None)
    category = relationship("Category", back_populates = "notes", cascade = "all, delete")


    def __repr__(self) -> str:
        return f"id: {self.id} - title: {self.title}"


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key = True, unique = True)
    file_path = Column(String, nullable = False)
    file_name = Column(String, unique = True, nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))


    def __repr__(self) -> str:
        return f"id: {self.id} - title: {self.file_name}"


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key = True, unique = True)
    title = Column(String(LIMIT_CATEGORY_TITLE), nullable = False)
    slug = Column(String(LIMIT_CATEGORY_SLUG), unique = True, nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    notes = relationship("Note", back_populates = "category")


    def __repr__(self) -> str:
        return f"title: {self.title} - slug: {self.slug}"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True, unique = True)
    username = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    email = Column(String, nullable = True)
    notes = relationship("Note", backref = "user_notes", cascade = "all, delete")
    files = relationship("File", backref = "user_files", cascade = "all, delete")
    categories = relationship("Category", backref = "user_categories", cascade = "all, delete")


    def __repr__(self) -> str:
        return f"id: {self.id} - username: {self.username}"
