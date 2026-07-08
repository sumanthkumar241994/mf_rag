from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CustomerPreferences:
    push_notifications_enabled: bool = False
    newsletter_enabled: bool = False
    summary_day: str | None = None
    reminder_days: int | None = None
    payment_preference: str | None = None