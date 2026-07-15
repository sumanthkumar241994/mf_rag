import asyncio
import json
from dataclasses import asdict
from datetime import datetime
from enum import Enum

from app.core.config.aws import AWS
from app.core.config.settings import settings

from app.events.models.base_event import BaseEvent
from app.events.publishers.base import EventPublisher
from app.events.models.event_priority import EventPriority

class SQSEventPublisher(EventPublisher):

    def __init__(self):
        self.sqs_client = AWS().sqs
        self.queue_urls = {
            EventPriority.HIGH.value : settings.HIGH_PRIORITY_QUEUE_URL,
            EventPriority.MEDIUM.value: settings.MEDIUM_PRIORITY_QUEUE_URL,
            EventPriority.LOW.value: settings.LOW_PRIORITY_QUEUE_URL
        }

    async def publish(self, event: BaseEvent):
        """
        Publish an event to appropriate to SQS queue based on its priority
        """
        queue_url = self.queue_urls.get(event.priority)

        if not queue_url:
            raise ValueError(f"No SQS queue configured for priority '{event.priority}'")
        
        payload = self._serialize(event)
        message_attributes = {
                "event_type": {
                    "DataType": "String",
                    "StringValue": event.event_type
                },
                "priority": {
                    "DataType": "String",
                    "StringValue": event.priority
                }
            }
        if event.correlation_id:
            message_attributes["correlation_id"] = {
                    "DataType": "String",
                    "StringValue": event.correlation_id,
                }

        await asyncio.to_thread(
            self.sqs_client.send_message,
            QueueUrl=queue_url,
            MessageBody=json.dumps(payload),
            MessageAttributes=message_attributes
        )


    def _serialize(self, event: BaseEvent) -> dict:
        """
        Converts dataclass events into JSON serializable dict
        """
        payload = asdict(event)
        return self._serialize_value(payload)

    
    def _serialize_value(self, value):
        if isinstance(value, datetime):
            return value.isoformat()

        if isinstance(value, Enum):
            return value.value

        if isinstance(value, dict):
            return {
                key: self._serialize_value(val) for key, val in value.items() 
            }
        
        if isinstance(value, list):
            return [
                self._serialize_value(item) for item in value
            ]
        
        return value