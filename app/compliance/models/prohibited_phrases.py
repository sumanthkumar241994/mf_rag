from dataclasses import dataclass
from re import Pattern
from typing import Generic, TypeVar

from app.compliance.enums.compliance_action import ComplianceAction
from app.compliance.enums.severity import Severity


T = TypeVar("T", str, Pattern[str])


@dataclass(slots=True, frozen=True)
class ProhibitedPhrase(Generic[T]):
    pattern: T
    description: str
    severity: Severity
    action: ComplianceAction
    replacement: str | None = None


@dataclass(slots=True, frozen=True)
class ProhibitedPhrases(Generic[T]):
    blocked: list[ProhibitedPhrase[T]]