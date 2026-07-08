from app.business.scheme.enums.lookup_type import LookupType
from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parsers.base_parser import BaseParser


class SchemeTypeParser(BaseParser):
    def parse(self, context: ParserContext):
        match = self.find_lookup_match(LookupType.SCHEME_TYPE, context.cleaned_query)

        if not match:
            return
        
        keyword, scheme_type = match
        if scheme_type not in context.scheme_types:
            context.scheme_types.append(scheme_type)
            
        context.matches['scheme_type'] = keyword
