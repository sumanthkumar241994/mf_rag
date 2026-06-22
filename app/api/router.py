from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.retrieval import router as retrieval_router

api_router = APIRouter()

api_router.include_router(
    health_router,
    prefix='/health',
    tags=['Health']
)

api_router.include_router(
    retrieval_router,
    prefix='/retrieval',
    tags=['Retrieval']
)