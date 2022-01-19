from datetime import datetime

from sqlalchemy import (
	Column, Integer, String,
	DateTime, Text
)

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.ext.declarative import declarative_base

from config import (
    BD_NAME, LIMIT_TITLE, LIMIT_TEXT
)


engine = create_async_engine(f"sqlite+aiosqlite:///db/{BD_NAME}.db")
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


    def __repr__(self) -> str:
        return f"<id: {self.id}> - <title: {self.title}>"
