from pydantic import BaseModel

from app.quality.feedback.enums.insight import FeedbackIssueAction
from app.quality.feedback.models.feedback_issue import FeedbackIssue
from app.quality.feedback.models.feedback_occurence import FeedbackOccurrence



class FeedbackIssueResult(BaseModel):
    issue: FeedbackIssue
    occurrence: FeedbackOccurrence
    action: FeedbackIssueAction