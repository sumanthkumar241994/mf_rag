import logging
from fastapi import APIRouter, Depends

from app.schemas.requests.retrieval import RetrievalRequest
from app.retrieval.retrieval_service import RetrievalService
from app.api.dependencies import get_retrieval_service
from app.core.config.aws import AWS

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/test")
async def retrieval_test(request: RetrievalRequest, retrieval_service: RetrievalService = Depends(get_retrieval_service)):
    return await retrieval_service.retrieve(
        query=request.query,
        top_k=request.top_k,
        scheme_name=request.scheme_name,
        document_type=request.document_type
    )
