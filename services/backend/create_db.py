import asyncio

from models.models import Base
from models.models import engine


async def main():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
	asyncio.run(main())
