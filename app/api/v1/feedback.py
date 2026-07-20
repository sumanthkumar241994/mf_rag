from fastapi import APIRouter, Depends, status

from app.api.dependencies.feedback import get_feedback_service
from app.api.dependencies.request_context import get_customer_id
from app.quality.feedback.feedback_service import FeedbackService
from app.quality.feedback.models.feedback import Feedback
from app.quality.feedback.models.feedback_response import FeedbackResponse
from app.quality.feedback.models.submit_feedback_request import SubmitFeedbackRequest


router = APIRouter()

@router.post(
    "",
    response_model=FeedbackResponse,
    status_code=status.HTTP_200_OK,
)
async def submit_feedback(
    request: SubmitFeedbackRequest,
    customer_id=Depends(get_customer_id),
    service: FeedbackService = Depends(get_feedback_service),
) -> Feedback:
    return await service.submit_feedback(
        customer_id=customer_id,
        request=request,
    )