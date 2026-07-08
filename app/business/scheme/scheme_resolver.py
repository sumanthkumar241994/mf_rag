# app/business/scheme/resolver/scheme_resolver.py

from app.business.scheme.models.scheme_query import SchemeQuery
from app.business.scheme.models.scheme_summary import SchemeSummary


class SchemeResolver:
    """
    Resolves Falcon search results into the schemes whose
    details should be fetched.

    Responsibilities
    ----------------
    - Resolve a single information query
    - Resolve comparison queries
    - Resolve recommendation queries

    Future
    ------
    - Prefer Regular plans
    - Prefer Growth unless IDCW requested
    - Similarity scoring
    - Human approval for ambiguous matches
    """

    def resolve(
        self,
        search_results: list[list[SchemeSummary]],
        query: SchemeQuery,
    ) -> list[SchemeSummary]:

        if not search_results:
            return []

        if query.recommendation:
            return self._resolve_recommendations(
                search_results,
                query,
            )

        if query.compare:
            return self._resolve_comparison(
                search_results,
                query,
            )

        return self._resolve_information(
            search_results,
            query,
        )

    # ------------------------------------------------------------------ #

    def _resolve_information(
        self,
        search_results: list[list[SchemeSummary]],
        query: SchemeQuery,
    ) -> list[SchemeSummary]:
        """
        Information query.

        Example
        -------
        Tell me about HDFC Balanced Advantage Fund
        """

        first_group = search_results[0]

        if not first_group:
            return []

        return [first_group[0]]

    # ------------------------------------------------------------------ #

    def _resolve_comparison(
        self,
        search_results: list[list[SchemeSummary]],
        query: SchemeQuery,
    ) -> list[SchemeSummary]:
        """
        Comparison query.

        Example
        -------
        Compare HDFC Balanced Advantage and
        ICICI Balanced Advantage

        One scheme is selected from every search result group.
        """

        resolved: list[SchemeSummary] = []

        for group in search_results:

            if not group:
                continue

            resolved.append(group[0])

        return resolved

    # ------------------------------------------------------------------ #

    def _resolve_recommendations(
        self,
        search_results: list[list[SchemeSummary]],
        query: SchemeQuery,
    ) -> list[SchemeSummary]:
        """
        Recommendation query.

        Example
        -------
        Recommend 5 ELSS funds.

        Recommendation queries generally have a single search result
        group returned by the search API.
        """

        first_group = search_results[0]

        return first_group[: query.max_results]