from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parsers.base_parser import BaseParser


class ConfidenceParser(BaseParser):
    def parse(self, context: ParserContext):
        confidence = 0.0

        if context.compare:
            confidence += 0.15

        if context.recommendation:
            confidence += 0.15
        
        if context.scheme_names:
            confidence += 0.35
        
        if context.categories:
            confidence += 0.10
        
        if context.scheme_types:
            confidence += 0.10
        
        if context.amc_names:
            confidence += 0.10
        
        if context.rating:
            confidence += 0.05
        
        if context.investment_option:
            confidence += 0.05

        context.confidence = min(confidence, 1.0)
