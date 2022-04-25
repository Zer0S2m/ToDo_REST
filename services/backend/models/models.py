from sqlalchemy import (
	Column, Integer, String,
	DateTime, Text, ForeignKey
)

from sqlalchemy.orm import (
	sessionmaker, relationship
)

from sqlalchemy.ext.asyncio import (
	create_async_engine, AsyncSession
)

from sqlalchemy.ext.declarative import declarative_base

from config import (
	BD_NAME, LIMIT_NOTE_TITLE, LIMIT_NOTE_TEXT,
	LIMIT_CATEGORY_TITLE, LIMIT_CATEGORY_SLUG,
	LIMIT_TITLE_PROJECT, LIMIT_SLUG_PROJECT, LIMIT_DESCRIPTION_PROJECT,
	LIMIT_TITLE_PART, LIMIT_SLUG_PART, LIMIT_DESCRIPTION_PART,
	LIMIT_TEXT_COMMENT,
)


engine = create_async_engine(f"sqlite+aiosqlite:///{BD_NAME}.db")
Session = sessionmaker(
	bind = engine, expire_on_commit = False, class_ = AsyncSession
)
Base = declarative_base()


class Note(Base):
	__tablename__ = "note"

	id = Column(Integer, primary_key = True, unique = True)
	title = Column(String(LIMIT_NOTE_TITLE), nullable = True, default = None)
	text = Column(Text(LIMIT_NOTE_TEXT), nullable = False)
	pub_date = Column(DateTime)
	importance = Column(Integer, default = 0)
	file_id = Column(Integer, ForeignKey('file.id', ondelete = "CASCADE"), default = False)
	file = relationship("File", backref = "note_file", cascade = "all, delete", lazy = "selectin")
	user_id = Column(Integer, ForeignKey('user.id'))
	category_id = Column(Integer, ForeignKey('category.id', ondelete = "CASCADE"), nullable = True, default = None)
	category = relationship("Category", back_populates = "notes", lazy = "selectin")
	part_id = Column(Integer, ForeignKey('part.id', ondelete = "CASCADE"), nullable = False)
	project_id = Column(Integer, ForeignKey("project.id", ondelete = "CASCADE"), nullable = False)

	def __repr__(self) -> str:
		return f"id: {self.id} - title: {self.title}"

	@property
	def as_dict(self):
		return {_cls.name: getattr(self, _cls.name) for _cls in self.__table__.columns}


class File(Base):
	__tablename__ = "file"

	id = Column(Integer, primary_key = True, unique = True)
	file_path = Column(String, nullable = False)
	file_name = Column(String, unique = True, nullable = False)
	user_id = Column(Integer, ForeignKey('user.id'))

	def __repr__(self) -> str:
		return f"id: {self.id} - title: {self.file_name}"

	@property
	def as_dict(self):
		return {_cls.name: getattr(self, _cls.name) for _cls in self.__table__.columns}


class Category(Base):
	__tablename__ = "category"

	id = Column(Integer, primary_key = True, unique = True)
	title = Column(String(LIMIT_CATEGORY_TITLE), nullable = False)
	slug = Column(String(LIMIT_CATEGORY_SLUG), unique = True, nullable = False)
	user_id = Column(Integer, ForeignKey('user.id'))
	notes = relationship("Note", back_populates = "category")
	project_id = Column(Integer, ForeignKey("project.id"))

	def __repr__(self) -> str:
		return f"title: {self.title} - slug: {self.slug}"

	@property
	def as_dict(self):
		return {_cls.name: getattr(self, _cls.name) for _cls in self.__table__.columns}


class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key = True, unique = True)
	username = Column(String, nullable = False, unique = True)
	password = Column(String, nullable = False)
	email = Column(String, nullable = True)
	notes = relationship("Note", backref = "user_notes", cascade = "all, delete")
	files = relationship("File", backref = "user_files", cascade = "all, delete")
	categories = relationship("Category", backref = "user_categories", cascade = "all, delete")
	projects = relationship("Project", backref = "user_projects", cascade = "all, delete")
	comments = relationship("Comment", backref = "user_comments", cascade = "all, delete")
	parts = relationship("Part", backref = "user_parts", cascade = "all, delete")

	def __repr__(self) -> str:
		return f"id: {self.id} - username: {self.username}"

	@property
	def as_dict(self):
		return {_cls.name: getattr(self, _cls.name) for _cls in self.__table__.columns}


class Project(Base):
	__tablename__ = "project"

	id = Column(Integer, primary_key = True, unique = True)
	title = Column(String(LIMIT_TITLE_PROJECT), nullable = False)
	slug = Column(String(LIMIT_SLUG_PROJECT), nullable = False)
	description = Column(Text(LIMIT_DESCRIPTION_PROJECT), nullable = False)
	pub_date = Column(DateTime)
	user_id = Column(Integer, ForeignKey('user.id'))
	comments = relationship("Comment", backref = "project_comments", cascade = "all, delete")
	parts = relationship(
		"Part",
		backref = "project_parts",
		cascade = "all, delete",
		order_by = "desc(Part.pub_date)"
	)
	categories = relationship("Category", backref = "project_categories", cascade = "all, delete")
	notes = relationship("Note", backref = "project_notes", cascade = "all, delete")

	def __repr__(self) -> str:
		return f"id: {self.id} - title: {self.title}"

	@property
	def as_dict(self):
		return {_cls.name: getattr(self, _cls.name) for _cls in self.__table__.columns}


class Comment(Base):
	__tablename__ = "comment"

	id = Column(Integer, primary_key = True, unique = True)
	user_id = Column(Integer, ForeignKey('user.id'))
	project_id = Column(Integer, ForeignKey('project.id'))
	text = Column(Text(LIMIT_TEXT_COMMENT), nullable = False)
	pub_date = Column(DateTime)

	def __repr__(self) -> str:
		return f"id: {self.id}"

	@property
	def as_dict(self):
		return {_cls.name: getattr(self, _cls.name) for _cls in self.__table__.columns}


class Part(Base):
	__tablename__ = "part"

	id = Column(Integer, primary_key = True, unique = True)
	title = Column(String(LIMIT_TITLE_PART), nullable = False)
	slug = Column(String(LIMIT_SLUG_PART), nullable = False)
	pub_date = Column(DateTime)
	description = Column(Text(LIMIT_DESCRIPTION_PART), nullable = False)
	user_id = Column(Integer, ForeignKey('user.id'))
	project_id = Column(Integer, ForeignKey('project.id'))
	notes = relationship(
		"Note",
		backref = "part_notes",
		cascade = "all, delete",
		order_by = "desc(Note.pub_date)"
	)

	def __repr__(self) -> str:
		return f"id: {self.id} - title: {self.title}"

	@property
	def as_dict(self):
		return {_cls.name: getattr(self, _cls.name) for _cls in self.__table__.columns}

	@property
	def serialize_project_main(self):
		return {
			"title": self.title,
			"slug": self.slug,
			"id": self.id
		}
