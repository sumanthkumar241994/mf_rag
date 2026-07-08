from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Investment:
    investment_allowed: bool = False
    has_investments: bool = False
    risk_profile: str | None = None
    last_payment_mode: str | None = None
    regular_investment_allowed: bool = False
    direct_plan_enabled: bool = False
    regular_plan_enabled: bool = False