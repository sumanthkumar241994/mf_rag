from dataclasses import dataclass, field
from typing import Any

from app.business.scheme.enums.scheme_sort import SchemeSort
from app.business.scheme.models.token import Token


@dataclass(slots=True)
class ParserContext:
    """
    Mutable working context used while parsing
    a natural language scheme query.
    """
    raw_query: str
    cleaned_query: str = ""
    tokens: list[Token] = field(default_factory=list)

    q: list[str] = field(default_factory=list)

    compare: bool = False
    recommendation: bool = False

    matches: dict[str, Any] = field(default_factory=dict)

    scheme_names: list[str] = field(default_factory=list)

    categories: list[str] = field(default_factory=list)
    scheme_types: list[str] = field(default_factory=list)
    amc_names: list[str] = field(default_factory=list)

    rating: int | None = None
    riskometer: int | None = None

    investment_option: str | None = None

    max_results: int = 1
    page: int = 1

    sort: SchemeSort = SchemeSort.RELEVANCE
    confidence: float = 1.0

    matches: dict[str, object] = field(default_factory=dict)