from app.dtos.jira_feedback_webhook import JiraFeedbackWebhookRequest
from app.unit_of_work.feedback_insight_uow import FeedbackInsightUnitOfWork


class FeedbackWebhookService:

    def __init__(
        self,
        uow: FeedbackInsightUnitOfWork,
    ):
        self._uow = uow

    async def jira_created(
        self,
        request: JiraFeedbackWebhookRequest,
    ) -> None:

        async with self._uow:

            issue = await self._uow.feedback_issues.get_by_id(
                request.feedback_issue_id
            )

            if issue is None:
                raise ValueError("Feedback issue not found")

            issue.jira_key = request.jira_key
            issue.jira_url = request.jira_url

            await self._uow.feedback_issues.save(issue)

            await self._uow.commit()