# app/business/scheme/parsers/rating_parser.py

import re

from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parsers.base_parser import BaseParser


class RatingParser(BaseParser):

    RATING_PATTERN = re.compile(
        r"(?:rating|rated)?\s*([1-5])\s*-?\s*stars?",
        re.IGNORECASE,
    )

    def parse(
        self,
        context: ParserContext,
    ) -> None:

        match = self.RATING_PATTERN.search(
            context.cleaned_query,
        )

        if not match:
            return

        context.rating = int(match.group(1))

        context.matches["rating"] = match.group(0)