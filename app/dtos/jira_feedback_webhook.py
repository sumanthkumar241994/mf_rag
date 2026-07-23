# app/api/models/webhooks.py

from pydantic import BaseModel
from uuid import UUID


class JiraFeedbackWebhookRequest(BaseModel):
    feedback_issue_id: UUID

    jira_key: str
    jira_url: str