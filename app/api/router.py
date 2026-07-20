from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.retrieval import router as retrieval_router
from app.api.v1.advisor import router as advisor_router
from app.api.v1.feedback import router as feedback_router

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

api_router.include_router(
    advisor_router,
    prefix="/advisor",
    tags=['advisor']
)

api_router.include_router(
    feedback_router,
    prefix="/feedback",
    tags=["Feedback"]
)
