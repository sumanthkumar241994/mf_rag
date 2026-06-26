# app/workers/bootstrap.py
from app.langfuse.client import langfuse_client

from app.events.consumers.sqs_consumer import SQSConsumer
from app.events.dispatcher.event_dispatcher import EventDispatcher

from app.events.handlers.langfuse_handler import LangfuseHandler

from app.workers.event_worker import EventWorker


def get_event_worker() -> EventWorker:
    dispatcher = EventDispatcher()

    dispatcher.register("llm.generation.completed", LangfuseHandler(langfuse=langfuse_client))

    consumer = SQSConsumer()

    return EventWorker(consumer, dispatcher)