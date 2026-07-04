from enum import StrEnum


class ApprovalDecision(StrEnum):
    AUTO ='auto'
    HUMAN_REVIEW = 'human_review'
    REJECT = 'reject'