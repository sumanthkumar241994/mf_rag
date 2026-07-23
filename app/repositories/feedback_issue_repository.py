from dataclasses import asdict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback_issue import FeedbackIssueModel
from app.quality.feedback.enums.insight import FeedbackIssueStatus, IssueCategory, RootCause
from app.quality.feedback.models.feedback import Feedback
from app.quality.feedback.models.feedback_insight import FeedbackInsight
from app.quality.feedback.models.feedback_issue import FeedbackIssue



class FeedbackIssueRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get_by_id(
        self,
        issue_id: UUID,
    ) -> FeedbackIssueModel | None:

        stmt = (
            select(FeedbackIssueModel)
            .where(
                FeedbackIssueModel.id == issue_id,
            )
        )

        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return Feedback.model_validate(model)

    async def find_active_issue(
        self,
        category: IssueCategory,
        root_cause: RootCause,
    ) -> FeedbackInsight | None:

        stmt = (
            select(FeedbackIssueModel)
            .where(
                FeedbackIssueModel.category == category,
                FeedbackIssueModel.root_cause == root_cause,
                FeedbackIssueModel.status.in_(
                    [
                        FeedbackIssueStatus.OPEN.value,
                        FeedbackIssueStatus.IN_PROGRESS.value,
                    ]
                ),
            )
        )

        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return FeedbackIssue.model_validate(model)

    async def save(
        self,
        issue: FeedbackIssue,
    ) -> FeedbackIssue:

        stmt = (
            select(FeedbackIssueModel)
            .where(
                FeedbackIssueModel.id == issue.id,
            )
        )

        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            model = FeedbackIssueModel(**asdict(issue))
            self.db.add(model)

        else:
            update_data = asdict(issue)
            update_data.pop("id", None)
            update_data.pop("created_at", None)

            for field, value in update_data.items():
                setattr(model, field, value)

        await self.db.flush()
        await self.db.refresh(model)

        return FeedbackIssue(
            id=model.id,
            category=model.category,
            root_cause=model.root_cause,
            severity=model.severity,
            jira_key=model.jira_key,
            status=model.status,
            occurrence_count=model.occurrence_count,
            first_seen=model.first_seen,
            last_seen=model.last_seen,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )