# app/business/scheme/parsers/investment_option_parser.py

from app.business.scheme.enums.investment_option import InvestmentOption
from app.business.scheme.enums.lookup_type import LookupType
from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parsers.base_parser import BaseParser


class InvestmentOptionParser(BaseParser):

    def parse(
        self,
        context: ParserContext,
    ) -> None:
        return
        # match = self.find_lookup_match(
        #     LookupType.INVESTMENT_OPTION,
        #     context.cleaned_query,
        # )

        # if not match:
        #     return

        # keyword, option = match

        # context.investment_option = InvestmentOption(option)

        # context.matches["investment_option"] = keyword