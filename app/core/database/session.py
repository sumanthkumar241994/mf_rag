from sqlalchemy.ext.asyncio import (
    async_sessionmaker, 
    AsyncSession, 
    create_async_engine)

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=False)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


