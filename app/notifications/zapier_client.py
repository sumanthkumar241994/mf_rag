import httpx

from app.core.config import settings

from .base import BaseNotificationClient
from .models import NotificationEvent


class ZapierClient(BaseNotificationClient):

    def __init__(
        self,
        webhook_url: str
    ):
        self._webhook_url = webhook_url

    async def notify(
        self,
        event: NotificationEvent,
    ) -> None:

        async with httpx.AsyncClient(timeout=10) as client:

            response = await client.post(
                self._webhook_url,
                json={
                    "event": event.event,
                    "severity": event.severity,
                    "title": event.title,
                    "description": event.description,
                    "metadata": event.metadata,
                },
            )

            response.raise_for_status()