from enum import StrEnum


class IssueCategory(StrEnum):
    PLANNER = "planner"
    RETRIEVAL = "retrieval"
    PROMPT = "prompt"
    BUSINESS = "business"
    KNOWLEDGE = "knowledge"
    OTHER = "other"

class RootCause(StrEnum):
    PLANNER_PORTFOLIO_IGNORED = "planner_portfolio_ignored"
    PLANNER_RISK_PROFILE_IGNORED = "planner_risk_profile_ignored"
    PLANNER_GOAL_IGNORED = "planner_goal_ignored"
    RETRIEVAL_NO_CONTEXT = "retrieval_no_context"
    PROMPT_GENERIC_RESPONSE = "prompt_generic_response"
    BUSINESS_INCORRECT_RECOMMENDATION = "business_incorrect_recommendation"
    UNKNOWN = "unknown"

class FeedbackIssueStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class FeedbackIssueAction(StrEnum):
    CREATED = "created"
    UPDATED = "updated"