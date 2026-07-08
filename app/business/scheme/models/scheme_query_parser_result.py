from dataclasses import dataclass
from typing import Any

from app.business.scheme.models.scheme_query import SchemeQuery


@dataclass(slots=True)
class SchemeQueryParserResult:
    query: SchemeQuery
    confidence: float
    matches: dict[str, Any]