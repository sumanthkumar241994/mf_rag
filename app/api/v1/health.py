import logging
from fastapi import APIRouter, Request

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("")
async def health_check(request: Request):
    return {"status": "ok"}