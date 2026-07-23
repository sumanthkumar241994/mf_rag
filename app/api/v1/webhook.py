from fastapi import APIRouter, Depends

from app.api.dependencies.feedback_webhook import get_feedback_webhook_service
from app.dtos.jira_feedback_webhook import JiraFeedbackWebhookRequest
from app.services.feedback_webhook_service import FeedbackWebhookService

router = APIRouter()


@router.post("/feedback")
async def jira_feedback_webhook(
    request: JiraFeedbackWebhookRequest,
    service: FeedbackWebhookService = Depends(get_feedback_webhook_service),
):

    await service.jira_created(request)

    return {
        "success": True,
    }