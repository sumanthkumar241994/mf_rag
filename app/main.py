from doctest import Example
from sqlalchemy import text
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic_settings.main import re
from app.core.config import settings
from app.core.middleware import register_tracing_middleware, register_logging_middleware
from app.core.database import AsyncSessionLocal
from app.api.dependencies import DBSession
from app.observability import setup_logging
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """startup and shutdown events"""
    try:
        async with AsyncSessionLocal.begin() as conn:
            await conn.execute(text("SELECT 1"))
            logger.info("Postgres connection established")
    except Exception as ex:
        logger.error("Database connection failed")
        raise

    yield
    await DBSession.dispose()
    print("Shutting down...")

def create_application() -> FastAPI:
    app = FastAPI(lifespan=lifespan, 
                title=settings.APP_NAME,
                description=settings.APP_DESCRIPTION, 
                version=settings.APP_VERSION, 
                docs_url=settings.APP_DOCS_URL, 
                redoc_url=settings.APP_REDOC_URL
                )
    setup_logging()
    register_tracing_middleware(app)
    register_logging_middleware(app)

    return app

app = create_application()

@app.get("/health")
async def health_check(db: DBSession):
    return {"status": "ok"}



