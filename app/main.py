from doctest import Example
from sqlalchemy import text
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from pydantic_settings.main import re
from app.core.config import settings
from app.core.middleware import (
    register_tracing_middleware, 
    register_logging_middleware,
    register_authentication_middleware,
    register_session_middleware
)
from app.api.router import api_router
from app.core.database import AsyncSessionLocal, engine
from app.api.dependencies import DBSession
from app.observability import setup_logging

from app.langfuse.client import langfuse_client
import logging

logger = logging.getLogger(__name__)

# import debugpy

# debugpy.listen(("0.0.0.0", 5679))
# print("⏳ Waiting for debugger to attach...")
# debugpy.wait_for_client()  # Execution will pause here until debugger is attached
# print("✅ Debugger Attached. Running Falcon App...")

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

    _ = langfuse_client

    yield
    await engine.dispose()
    langfuse_client.flush()
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
    register_session_middleware(app)
    register_authentication_middleware(app)

    app.include_router(
        api_router,
        prefix='/api/v1'
    )

    return app

app = create_application()



