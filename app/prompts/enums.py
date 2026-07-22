from enum import StrEnum


class PromptType(StrEnum):
    # Advisor
    ADVISOR = "advisor"

    # Planner
    PLANNER = "planner"

    # Conversation
    CONVERSATION_TITLE = "conversation_title"
    CONVERSATION_SUMMARY = "conversation_summary"

    # Evaluation / Judges
    PLANNER_JUDGE = "planner_judge"
    RESPONSE_JUDGE = "response_judge"
    CONTEXT_JUDGE = "context_judge"
    RETRIEVAL_JUDGE = "retrieval_judge"
    GROUNDEDNESS_JUDGE = "groundedness_judge"
    HALLUCINATION_JUDGE = "hallucination_judge"
    RELEVANCE_JUDGE = "relevance_judge"
    FAITHFULNESS_JUDGE = "faithfulness_judge"