from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Generic, TypeVar

from app.business.customer.models.metadata import KnowledgeMetadata

T = TypeVar("T")

@dataclass(slots=True)
class KnowledgeValue(Generic[T]):
    """
    Represents one advisor knowledge attribute.
    """
    value: T | None = None
    metadata: KnowledgeMetadata = field(default_factory=KnowledgeMetadata)


@dataclass(slots=True)
class CustomerKnowledge:
    retirement_age: KnowledgeValue[int] = field(default_factory=KnowledgeValue)
    annual_income: KnowledgeValue[Decimal] = field(default_factory=KnowledgeValue)
    monthly_expense: KnowledgeValue[Decimal] = field(default_factory=KnowledgeValue)
    financial_dependents: KnowledgeValue[int] = field(default_factory=KnowledgeValue)
    investment_horizon: KnowledgeValue[int] = field(default_factory=KnowledgeValue)
    preferred_return_assumption: KnowledgeValue[float] = field(default_factory=KnowledgeValue)
