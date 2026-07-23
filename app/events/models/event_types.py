from enum import StrEnum


class EventType(StrEnum):
    BASE = 'base.event'
    LLM_GENERATION_COMPLETED = "llm.generation.completed"
    OBSERVATION_COMPLETED = "observation.completed"

    CONVERSATION_TITLE_GENERATE = "conversation.title.generate"
    CONVERSATION_SUMMARY_GENERATE = "conversation.summary.generate"

    MEMORY_EXTRACT = "memory.extract"

    EVALUATION_RUN = "evaluation.run"

    FEEDBACK_RECEIVED = "feedback.received"