import asyncio
import shutil
import os

from models.models import Base
from models.models import engine

from config.config import BD_NAME


async def main():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

	source_path = f"{BD_NAME}.db"

	if os.path.exists(source_path):
		os.mkdir("db")
		shutil.move(source_path, f"db\{source_path}")


if __name__ == '__main__':
	asyncio.run(main())
