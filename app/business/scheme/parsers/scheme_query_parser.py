from curses import raw
from app.business.advisor.enums.intent import Intent
from app.business.scheme.models.scheme_query import SchemeQuery
from app.business.scheme.models.scheme_query_parser_result import SchemeQueryParserResult
from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parser.tokenizer import Tokenizer
from app.business.scheme.parsers.amc_parser import AMCParser
from app.business.scheme.parsers.category_parser import CategoryParser
from app.business.scheme.parsers.comparision_parser import ComparisionParser
from app.business.scheme.parsers.confidence_parser import ConfidenceParser
from app.business.scheme.parsers.investment_option_parser import InvestmentOptionParser
from app.business.scheme.parsers.limit_parser import LimitParser
from app.business.scheme.parsers.normalization_parser import NormalizationParser
from app.business.scheme.parsers.rating_parser import RatingParser
from app.business.scheme.parsers.recommendation_parser import RecommendationParser
from app.business.scheme.parsers.scheme_name_parser import SchemeNameParser
from app.business.scheme.parsers.scheme_type_parser import SchemeTypeParser


class SchemeQueryParser:
    """
    Converts a natural language query into a structured SchemeQuery.

    Flow

        Query
            ↓
        Tokenizer
            ↓
        ParserContext
            ↓
        ComparisonParser
            ↓
        RecommendationParser
            ↓
        LimitParser
            ↓
        NormalizationParser
            ↓
        CategoryParser
            ↓
        SchemeTypeParser
            ↓
        AMCParser
            ↓
        RatingParser
            ↓
        InvestmentOptionParser
            ↓
        SchemeNameParser
            ↓
        ConfidenceParser
            ↓
        SchemeQuery
    """

    def __init__(
        self,
        tokenizer : Tokenizer,
        comparision_parser: ComparisionParser,
        recommendation_parser: RecommendationParser,
        limit_parser: LimitParser,
        normalization_parser: NormalizationParser,
        category_parser: CategoryParser,
        scheme_type_parser: SchemeTypeParser,
        amc_parser: AMCParser,
        rating_parser: RatingParser,
        investment_option_parser: InvestmentOptionParser,
        scheme_name_parser: SchemeNameParser,
        confidence_parser: ConfidenceParser
    ):
        self.tokenizer = tokenizer
        self.parsers =[ 
            comparision_parser,
            recommendation_parser,
            limit_parser,
            normalization_parser,
            category_parser,
            scheme_type_parser,
            amc_parser,
            rating_parser,
            investment_option_parser,
            scheme_name_parser,
            confidence_parser
        ]
    
    def parse(self, query: str, intent: Intent | None = None) -> SchemeQueryParserResult:
        context = ParserContext(raw_query=query)

        context.tokens = self.tokenizer.tokenize(query)
        #
        # Future
        #
        # if intent:
        #     context.intent = intent
        #

        for parser in self.parsers:
            parser.parse(context)
        
        scheme_query = SchemeQuery(
            raw_query=context.raw_query,
            q=context.scheme_names.copy(),
            scheme_names=context.scheme_names,
            categories=context.categories,
            scheme_types=context.scheme_types,
            amc_names=context.amc_names,
            rating=context.rating,
            riskometer=context.riskometer,
            investment_option=context.investment_option,
            compare=context.compare,
            recommendation=context.recommendation,
            max_results=context.max_results,
            page=context.page,
            sort=context.sort
        )
        
        return SchemeQueryParserResult(scheme_query, context.confidence, context.matches)