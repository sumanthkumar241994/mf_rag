from abc import ABC, abstractmethod

from .models import NotificationEvent


class BaseNotificationClient:

    @abstractmethod
    async def notify(
        self,
        event: NotificationEvent,
    ) -> None:
        ...