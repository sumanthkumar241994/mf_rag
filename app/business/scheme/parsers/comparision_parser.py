from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parsers.base_parser import BaseParser


class ComparisionParser(BaseParser):
    KEYWORDS = {
        "compare",
        "vs",
        "versus",
        "against"
    }

    def parse(self, context: ParserContext):
        query = context.raw_query.lower()

        context.compare = any(keyword in query for keyword in self.KEYWORDS)

        if context.compare:
            context.matches['comparision'] = True