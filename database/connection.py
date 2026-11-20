from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from database.models import Base

DATABASE_URL = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def initialize_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def close_database():
    await engine.dispose()
