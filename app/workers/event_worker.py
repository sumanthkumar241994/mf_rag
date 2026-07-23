# app/workers/event_worker.py

import logging
import asyncio
import traceback
from app.events.consumers.sqs_consumer import SQSConsumer
from app.events.dispatcher.event_dispatcher import EventDispatcher

from app.events.models.event_priority import EventPriority
from app.events.factory.event_factory import EventFactory

logger = logging.getLogger(__name__)


class EventWorker:
    def __init__(self, consumer: SQSConsumer, dispatcher: EventDispatcher):
        self.consumer = consumer
        self.dispatcher = dispatcher

    async def start(self):
        """
        Start polling all queues forever
        """
        print("Starting EventWorker")
        await asyncio.gather(
            self._poll_queues(EventPriority.HIGH.value),
            self._poll_queues(EventPriority.MEDIUM.value),
            self._poll_queues(EventPriority.LOW.value)
        )

    async def _poll_queues(self, priority: EventPriority):
        print(f"started polling {priority} queue")
        while True:
            try:
                print("Waiting for messages...")
                messages = await self.consumer.receive_messages(
                    priority=priority
                )

                if not messages:
                    continue

                for message in messages:
                    logger.info(f"Processing event_id: {message['Body']['event_id']} and event type: {message['Body']['event_type']}")
                    await self._process_message(prirority=priority, message=message)
            except Exception:
                print(f"Failed while polling {priority} queue")
                traceback.print_exc()
                await asyncio.sleep(5)


        
    async def _process_message(self, prirority: EventPriority, message: dict):
        receipt_handle = message['ReceiptHandle']

        try:
            body = self.consumer.get_body(message)
            event = EventFactory.from_dict(body)
            print("Dispatch started")
            await self.dispatcher.dispatch(event)
            print("Dispatch completed")
            await self.consumer.delete_message(
                priority=prirority,
                receipt_handle=receipt_handle
            )
        except Exception as ex:
            print(f"Failed processing message from {prirority} queue and exception {str(ex)}")
