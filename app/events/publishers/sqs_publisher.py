import asyncio
import json
from dataclasses import asdict
from datetime import datetime

from app.core.config.aws import AWS
from app.core.config.settings import settings

from app.events.models.base_event import BaseEvent
from app.events.publishers.base import EventPublisher
from app.events.models.event_priority import EventPriority

class SQSEventPublisher(EventPublisher):

    def __init__(self):
        self.sqs_client = AWS().sqs
        self.queue_urls = {
            EventPriority.HIGH : settings.HIGH_PRIORITY_QUEUE_URL,
            EventPriority.MEDIUM: settings.MEDIUM_PRIORITY_QUEUE_URL,
            EventPriority.LOW: settings.LOW_PRIORITY_QUEUE_URL
        }

    async def publish(self, event: BaseEvent):
        """
        Publish an event to appropriate to SQS queue based on its priority
        """
        queue_url = self.queue_urls.get(event.priority)

        if not queue_url:
            raise ValueError(f"No SQS queue configured for priority '{event.priority}'")
        
        payload = self._serialize(event)

        await asyncio.to_thread(
            self.sqs_client.send_message,
            QueueUrl=queue_url,
            MessageBody=json.dumps(payload),
            MessageAttributes={
                "event_type": {
                    "DataType": "String",
                    "StringValue": event.event_type
                },
                "priority": {
                    "DataType": "String",
                    "StringValue": event.priority
                },
                "correlation_id": {
                    "DataType": "String",
                    "StringValue": event.correlation_id
                }
            }
        )


    def _serialize(self, event: BaseEvent) -> dict:
        """
        Converts dataclass events into JSON serializable dict
        """
        payload = asdict(event)
        return self._convert_datetime(payload)

    
    def _convert_datetime(self, value):
        if isinstance(value, datetime):
            return value.isoformat()

        if isinstance(value, dict):
            return {
                key: self._convert_datetime(val) for key, val in value.items() 
            }
        
        if isinstance(value, list):
            return [
                self._convert_datetime(item) for item in value
            ]
        
        return value