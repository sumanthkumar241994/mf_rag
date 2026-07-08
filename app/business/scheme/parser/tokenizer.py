import re
from turtle import position

from app.business.scheme.models.token import Token


class Tokenizer:
    """
    Converts a natural language query into ordered tokens.

    The tokenizer is intentionally business agnostic.
    It performs lexical analysis only.
    """

    TOKEN_PATTERN = re.compile(
        r"""
        >=|<=|>|<|=|          # comparison operators
        \d+(?:\.\d+)?%?|      # numbers (15, 15.5, 15%)
        [A-Za-z][A-Za-z0-9.&'-]*|  # words
        [,()]                 # punctuation
        """,
        re.VERBOSE,
    )

    def tokenize(self, query: str) -> list[Token]:
        matches = self.TOKEN_PATTERN.findall(query)
        return [Token(text=match, normalized=match.lower(), position=index) for index, match in enumerate(matches)]
