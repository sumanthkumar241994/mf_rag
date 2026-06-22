import logging
from fastapi import APIRouter, Request

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
async def health_check(request: Request):
    logger.info(f"user: {request.state.customer_uid} and session: {request.state.session}")
    return {"status": "ok"}