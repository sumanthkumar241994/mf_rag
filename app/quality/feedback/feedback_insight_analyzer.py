from datetime import UTC, datetime

from app.quality.feedback.enums.insight import FeedbackIssueAction
from app.quality.feedback.models.feedback import Feedback
from app.quality.feedback.models.feedback_issue import FeedbackIssue
from app.quality.feedback.models.feedback_issue_result import FeedbackIssueResult
from app.quality.feedback.models.feedback_insight import FeedbackInsight
from app.quality.feedback.models.feedback_occurence import FeedbackOccurrence
from app.unit_of_work.feedback_insight_uow import FeedbackInsightUnitOfWork
from app.unit_of_work.feedback_insight_uow_factory import FeedbackInsightUnitOfWorkFactory


class FeedbackIssueAnalyzer:


    async def analyze(
        self,
        feedback: Feedback,
        insight: FeedbackInsight,
        uow: FeedbackInsightUnitOfWork
    ) -> FeedbackIssueResult:

        self.uow = uow

        issue = await self.uow.feedback_issues.find_active_issue(
            category=insight.category,
            root_cause=insight.root_cause,
        )

        if issue is None:
            issue = await self._create_issue(
                feedback=feedback,
                insight=insight,
            )   

            occurence = await self._save_occurrence(
                issue=issue,
                feedback=feedback,
                )

            return FeedbackIssueResult(
                issue=issue,
                occurrence=occurence,
                action=FeedbackIssueAction.CREATED,
            )

        issue = await self._update_issue(
            issue=issue,
            feedback=feedback,
        )

        occurence = await self._save_occurrence(
                issue=issue,
                feedback=feedback,
                )

        return FeedbackIssueResult(
            issue=issue,
            occurrence=occurence,
            action=FeedbackIssueAction.UPDATED,
        )

    async def _create_issue(
        self,
        feedback: Feedback,
        insight: FeedbackInsight,
    ) -> FeedbackIssue:

        now = datetime.now(UTC)

        issue = FeedbackIssue(
            category=insight.category,
            root_cause=insight.root_cause,
            severity=insight.severity,
            occurrence_count=1,
            first_seen=now,
            last_seen=now,
        )

        issue = await self.uow.feedback_issues.save(issue)


        return issue

    async def _update_issue(
        self,
        issue: FeedbackIssue,
        feedback: Feedback,
    ) -> FeedbackIssue:

        issue.occurrence_count += 1
        issue.last_seen = datetime.now(UTC)

        issue = await self.uow.feedback_issues.save(issue)

        await self._save_occurrence(
            issue=issue,
            feedback=feedback,
        )

        return issue

    async def _save_occurrence(
        self,
        issue: FeedbackIssue,
        feedback: Feedback,
    ) -> None:

        occurrence = FeedbackOccurrence(
            issue_id=issue.id,
            feedback_id=feedback.id,
            conversation_id=feedback.conversation_id,
            message_id=feedback.message_id,
            created_at=datetime.now(UTC),
        )

        occurrence = await self.uow.feedback_occurences.save(
            occurrence,
        )

        return occurrence