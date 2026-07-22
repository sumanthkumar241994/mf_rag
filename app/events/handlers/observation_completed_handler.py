from langfuse import Langfuse

from app.events.models.observation_complated_event import ObservationCompletedEvent

from app.events.handlers.base import EventHandler

import logging
logger = logging.getLogger(__name__)

class ObservationCompletedHandler(EventHandler[ObservationCompletedEvent]):
    """
    Publishes complete LLM generations to Langfuse
    """
    critical = True

    def __init__(self, langfuse: Langfuse):
        self.langfuse = langfuse


    async def handle(
        self,
        event: ObservationCompletedEvent,
    ):
        trace_context = {
            "trace_id": event.trace_id,
            "parent_observation_id": event.parent_observation_id,
        }

        try:
            with self.langfuse.start_as_current_observation(
                as_type="span",
                name=event.name,
                trace_context=trace_context,
                input=event.input,
                output=event.output,
                metadata=event.metadata,
            ) as observation:
                print(f"Observation: {observation}")

        except Exception as ex:
            print(
                f"Failed to publish observation: {ex}"
            )