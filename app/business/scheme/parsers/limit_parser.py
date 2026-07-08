from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parsers.base_parser import BaseParser


class LimitParser(BaseParser):
    DEFAULT_LIMIT = 1

    def parse(self, context: ParserContext):
        context.max_results = self.DEFAULT_LIMIT
        for token in context.tokens:
            if token.normalized.isdigit():
                context.max_results = int(token.normalized)
                context.matches['limit'] = token.text

                return