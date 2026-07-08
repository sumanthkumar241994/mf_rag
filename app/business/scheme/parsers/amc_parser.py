from app.business.scheme.enums.lookup_type import LookupType
from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parsers.base_parser import BaseParser


class AMCParser(BaseParser):
    def parse(self, context: ParserContext):
        match = self.find_lookup_match(lookup_type=LookupType.AMC, query=context.cleaned_query)

        if not match:
            return
        
        keyword, amc = match

        if amc not in context.amc_names:
            context.amc_names.append(amc)

        context.matches["amc"] = keyword