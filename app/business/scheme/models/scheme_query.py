from dataclasses import dataclass, field, replace

from app.business.scheme.enums.scheme_sort import SchemeSort


@dataclass(slots=True)
class SchemeQuery:
    raw_query: str

    q: list[str] = field(default_factory=list)

    scheme_names: list[str] = field(default_factory=list)

    categories: list[str] = field(default_factory=list)
    scheme_types: list[str] = field(default_factory=list)
    amc_names: list[str] = field(default_factory=list)

    rating: int | None = None
    riskometer: int | None = None

    investment_option: str | None = None

    compare: bool = False
    recommendation: bool = False

    max_results: int = 1
    page: int = 1

    sort: SchemeSort = SchemeSort.RELEVANCE

    def clone_for_scheme(self, scheme_name: str) -> "SchemeQuery":
        return replace(
            self, q=scheme_name, scheme_names=[scheme_name]
        )



