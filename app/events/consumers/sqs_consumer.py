import asyncio
import json
import queue
from typing import Any

from app.core.config.aws import AWS
from app.core.config.settings import settings
from app.events.models.queue_priority import QueuePriority

class SQSConsumer:
    """
    Thin wrapper around Amazon SQS.

    Responsible only for:
    - Receiving messages
    - Deleting messages
    """
    
    def __init__(self):
        self.sqs = AWS().sqs
        self.queue_urls = {
            QueuePriority.HIGH.value: settings.HIGH_PRIORITY_QUEUE_URL,
            QueuePriority.MEDIUM.value: settings.MEDIUM_PRIORITY_QUEUE_URL,
            QueuePriority.LOW.value: settings.LOW_PRIORITY_QUEUE_URL 
        }

    async def receive_messages(
        self,
        priority: QueuePriority,
        max_messages: int = 10,
        wait_time_seconds: int = 20,
        visibility_timeout: int = 60
        ) -> list[dict[str, any]]:
            """
            Recieve messages for a given priority queue
            """

            queue_url = self.queue_urls[priority]
            response = await asyncio.to_thread(
                self.sqs.receive_message,
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time_seconds,
                VisibilityTimeout=visibility_timeout,
                MessageAttributeNames=['All']
            )

            return response.get("Messages", [])

    async def delete_message(self, priority: QueuePriority, receipt_handle: str):
        queue_url = self.queue_urls[priority]

        await asyncio.to_thread(
            self.sqs.delete_message,
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
    
    @staticmethod
    def get_body(message: dict[str, Any]):
        """
        Deserialize SQS message body
        """
        return json.loads(message['Body'])