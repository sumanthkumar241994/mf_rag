# app/workers/bootstrap.py
from app.api.dependencies.conversation import build_conversation_title_service, build_conversation_summary_service
from app.events.handlers.conversation_service_handler import ConversationSummaryHandler
from app.events.handlers.conversation_title_handler import ConversationTitleHandler
from app.events.handlers.feedback_received_handler import FeedbackReceivedHandler
from app.events.handlers.observation_completed_handler import ObservationCompletedHandler
from app.events.models.event_types import EventType
from app.langfuse.client import langfuse_client

from app.events.consumers.sqs_consumer import SQSConsumer
from app.events.dispatcher.event_dispatcher import EventDispatcher

from app.events.handlers.langfuse_handler import LangfuseHandler

from app.workers.event_worker import EventWorker


def get_event_worker() -> EventWorker:
    dispatcher = EventDispatcher()

    dispatcher.register(EventType.LLM_GENERATION_COMPLETED, LangfuseHandler(langfuse=langfuse_client.client))
    dispatcher.register(EventType.CONVERSATION_TITLE_GENERATE,ConversationTitleHandler(title_service=build_conversation_title_service()))
    dispatcher.register(EventType.CONVERSATION_SUMMARY_GENERATE, ConversationSummaryHandler(summary_service=build_conversation_summary_service()))
    dispatcher.register(EventType.FEEDBACK_RECEIVED, FeedbackReceivedHandler())
    dispatcher.register(EventType.OBSERVATION_COMPLETED, ObservationCompletedHandler(langfuse=langfuse_client.client))

    consumer = SQSConsumer()

    return EventWorker(consumer, dispatcher)