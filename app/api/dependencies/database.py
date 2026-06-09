from collections.abc import AsyncGenerator
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import AsyncSessionLocal


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_db)]
