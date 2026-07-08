from app.business.scheme.enums.lookup_type import LookupType
from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parsers.base_parser import BaseParser


class CategoryParser(BaseParser):
    def parse(self, context: ParserContext):
        match = self.find_lookup_match(lookup_type=LookupType.CATEGORY, query=context.cleaned_query)

        if not match:
            return
        
        keyword, category = match
        if category not in context.categories:
            context.categories.append(category)
        context.matches['category'] = keyword