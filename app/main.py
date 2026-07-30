from doctest import Example
from fastmcp import FastMCP
from sqlalchemy import text
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from pydantic_settings.main import re
from app.api.dependencies.mcp import initialize_mcp
from app.api.dependencies.rest_api_client import get_rest_api_client
from app.composition.business.new_customer_composition import NewCustomerComposition
from app.composition.mcp_clients.mcp_composition import MCPComposition
from app.core.config import settings
from app.core.config.redis import get_redis
from app.core.middleware import (
    register_tracing_middleware, 
    register_request_context_middleware,
    register_authentication_middleware,
    register_session_middleware
)
from app.api.router import api_router
from app.core.database import AsyncSessionLocal, engine
from app.observability import setup_logging

from app.langfuse.client import langfuse_client
import logging

from app.infrastructure.workflow.workflow_checkpointer import workflow_checkpointer

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

    redis = get_redis()
    rest_api_client = get_rest_api_client()

    _ = langfuse_client.client

    await workflow_checkpointer.initialize()
    logger.info("Workflow checkpointer initalized")




    app.state.workflow_checkpointer = workflow_checkpointer.checkpointer

    # MCP Client
    mcp = MCPComposition()
    await mcp.client.startup()
    initialize_mcp(mcp.client)
    yield

    await workflow_checkpointer.shutdown()
    await engine.dispose()
    langfuse_client.client.flush()
    await mcp.client.shutdown()
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
    register_request_context_middleware(app)
    register_session_middleware(app)
    register_authentication_middleware(app)

    app.include_router(
        api_router,
        prefix='/api/v1'
    )

    return app

app = create_application()



