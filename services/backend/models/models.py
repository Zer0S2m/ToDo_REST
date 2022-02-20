from datetime import datetime
from email.policy import default

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
    BD_NAME, LIMIT_TITLE, LIMIT_TEXT
)


engine = create_async_engine(f"sqlite+aiosqlite:///{BD_NAME}.db")
Session = sessionmaker(
    engine, expire_on_commit = False, class_ = AsyncSession
)
Base = declarative_base()


class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key = True, unique = True)
    title = Column(String(LIMIT_TITLE), default = False)
    text = Column(Text(LIMIT_TEXT), nullable = False)
    pub_date = Column(DateTime, default = datetime.now())
    file = relationship("File", backref = "note_file", cascade = "all, delete")
    file_id = Column(Integer, ForeignKey('file.id', ondelete = "CASCADE"), default = False)


    def __repr__(self) -> str:
        return f"<id: {self.id}> - <title: {self.title}>"


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key = True, unique = True)
    file_path = Column(String, nullable = False)
    file_name = Column(String, unique = True, nullable = False)


    def __repr__(self) -> str:
        return f"<id: {self.id}> - <title: {self.file_name}>"
