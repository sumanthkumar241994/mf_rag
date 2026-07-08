# app/business/scheme/parser/query_normalizer.py

# app/business/scheme/parser/query_normalizer.py

import re
from dataclasses import dataclass

from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parsers.base_parser import BaseParser


@dataclass(frozen=True, slots=True)
class NormalizationRule:
    """
    Represents a single normalization rule.
    """
    pattern: str
    replacement: str


class NormalizationParser(BaseParser):
    """
    Normalizes a natural language query before parsing.

    Responsibilities:
        - Remove conversational prefixes
        - Normalize terminology
        - Normalize comparison keywords
        - Normalize recommendation keywords
        - Normalize whitespace
    """

    NORMALIZATION_RULES: list[NormalizationRule] = [

        # ------------------------------------------------------------------
        # Conversational prefixes
        # ------------------------------------------------------------------

        NormalizationRule(
            r"^tell me about\s+",
            "",
        ),
        NormalizationRule(
            r"^show me\s+",
            "",
        ),
        NormalizationRule(
            r"^give me\s+",
            "",
        ),
        NormalizationRule(
            r"^what is\s+",
            "",
        ),
        NormalizationRule(
            r"^details of\s+",
            "",
        ),
        NormalizationRule(
            r"^information about\s+",
            "",
        ),
        NormalizationRule(
            r"^can you show me\s+",
            "",
        ),
        NormalizationRule(
            r"^can you tell me about\s+",
            "",
        ),
        NormalizationRule(
            r"^please show\s+",
            "",
        ),
        NormalizationRule(
            r"^please tell me about\s+",
            "",
        ),

        # ------------------------------------------------------------------
        # Domain terminology
        # ------------------------------------------------------------------

        # NormalizationRule(
        #     r"\bmutual funds?\b",
        #     "scheme",
        # ),
        # NormalizationRule(
        #     r"\bfunds?\b",
        #     "scheme",
        # ),
        # NormalizationRule(
        #     r"\bmf\b",
        #     "scheme",
        # ),

        # ------------------------------------------------------------------
        # Investment option
        # ------------------------------------------------------------------

        NormalizationRule(
            r"\bgrowth option\b",
            "growth",
        ),
        NormalizationRule(
            r"\bidcw option\b",
            "idcw",
        ),

        # ------------------------------------------------------------------
        # Rating
        # ------------------------------------------------------------------

        NormalizationRule(
            r"(\d)\s*-\s*star",
            r"\1 star",
        ),
        NormalizationRule(
            r"(\d)\s*star",
            r"\1 star",
        ),

        # ------------------------------------------------------------------
        # Comparison
        # ------------------------------------------------------------------

        NormalizationRule(
            r"\bversus\b",
            "vs",
        ),
        NormalizationRule(
            r"\bagainst\b",
            "vs",
        ),

        # ------------------------------------------------------------------
        # Recommendation
        # ------------------------------------------------------------------

        NormalizationRule(
            r"\bbest\b",
            "top",
        ),
        NormalizationRule(
            r"\brecommended\b",
            "recommend",
        ),

        # ------------------------------------------------------------------
        # Whitespace
        # ------------------------------------------------------------------

        NormalizationRule(
            r"\s+",
            " ",
        ),
    ]

    def parse(
        self,
        context: ParserContext,
    ) -> str:
        """
        Normalize a user query before parsing.

        Examples
        --------
        Tell me about HDFC Balanced Advantage Fund
            -> hdfc balanced advantage scheme

        Compare HDFC versus ICICI
            -> compare hdfc vs icici

        Best Gold Mutual Funds
            -> top gold scheme
        """

        normalized = context.raw_query.strip().lower()

        for rule in self.NORMALIZATION_RULES:
            normalized = re.sub(
                rule.pattern,
                rule.replacement,
                normalized,
                flags=re.IGNORECASE,
            )

        context.cleaned_query = normalized.strip()
        context.matches['normalized_query'] = context.cleaned_query