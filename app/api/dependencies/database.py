from collections.abc import AsyncGenerator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.composition.database_composition import DatabaseComposition
from app.core.database import AsyncSessionLocal


_database: DatabaseComposition | None = None


def get_database() -> DatabaseComposition:
    global _database

    if _database is None:
        _database = DatabaseComposition(
            session_factory=AsyncSessionLocal,
        )

    return _database


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_db)]