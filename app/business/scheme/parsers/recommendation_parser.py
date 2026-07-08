from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parsers.base_parser import BaseParser


class RecommendationParser(BaseParser):
    KEYWORDS = {
        "recommend",
        "recommended",
        "top",
        "best",
        "good",
        "suggest"
    }

    def parse(self, context: ParserContext):
        query = context.raw_query.lower()

        context.recommendation = any( keyword in query for keyword in self.KEYWORDS)

        if context.recommendation:
            context.matches['recommendation'] = True