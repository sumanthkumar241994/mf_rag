from enum import StrEnum


class ToolType(StrEnum):
    """
    Executable business tools.

    A tool may implement one or more capabilities.
    """
    # Portfolio
    PORTFOLIO = "portfolio"
    # Customer
    CUSTOMER = "customer"
    # Investment Operations
    INVESTMENT = "investment"
    # Goal Planning
    GOAL = "goal"
    # Risk
    RISK = "risk"
    # Knowledge Base / RAG
    DOCUMENT_SEARCH = "document_search"
    # Market Intelligence
    MARKET = "market"
    # Advisor / Business Orchestration
    ADVISOR = "advisor"
    # User Feedback
    FEEDBACK = "feedback"
    # Ticketing
    JIRA = "jira"