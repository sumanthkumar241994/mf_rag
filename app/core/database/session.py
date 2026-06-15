from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession, 
    create_async_engine)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.core.config import settings

engine = create_async_engine(settings.ASYNC_DATABASE_URL, pool_pre_ping=True, echo=False)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

sync_engine = create_engine(settings.SYNC_DATABASE_URL, pool_pre_ping=True, echo=False)

SessionLocal = sessionmaker(bind=sync_engine, autoflush=False, autocommit=False)




