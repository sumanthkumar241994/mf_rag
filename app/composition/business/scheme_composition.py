

from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.tool_type import ToolType
from app.business.scheme.gateways.scheme_gateway import SchemeGateway
from app.business.scheme.mappers.scheme_mapper import SchemeMapper
from app.business.scheme.parser.static_lookup_provider import StaticLookupProvider
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
from app.business.scheme.parsers.scheme_query_parser import SchemeQueryParser
from app.business.scheme.parsers.scheme_type_parser import SchemeTypeParser
from app.business.scheme.scheme_resolver import SchemeResolver
from app.business.scheme.scheme_service import SchemeService
from app.tools.definitions.tool_definition import ToolDefinition
from app.tools.implementations.scheme_tool import SchemeTool


class SchemeComposition:

    def __init__(
        self,
        scheme_gateway:SchemeGateway
    ):

        self.lookup_provider = StaticLookupProvider()
        self.tokenizer = Tokenizer()

        self.normalization_parser = NormalizationParser()
        self.comparision_parser = ComparisionParser()
        self.recommendation_parser = RecommendationParser()
        self.category_parser = CategoryParser(
            lookup_provider=self.lookup_provider
        )

        self.amc_parser = AMCParser(lookup_provider=self.lookup_provider)
        self.scheme_type_parser = SchemeTypeParser(lookup_provider=self.lookup_provider)
        self.rating_parser = RatingParser()
        self.investment_option_parser = InvestmentOptionParser()
        self.scheme_name_parser = SchemeNameParser()
        self.limit_parser = LimitParser()
        self.confidence_parser = ConfidenceParser()

        self.query_parser = SchemeQueryParser(
            tokenizer=self.tokenizer,
            normalization_parser=self.normalization_parser,
            comparision_parser=self.comparision_parser,
            recommendation_parser=self.recommendation_parser,
            category_parser=self.category_parser,
            amc_parser=self.amc_parser,
            scheme_type_parser=self.scheme_type_parser,
            rating_parser=self.rating_parser,
            investment_option_parser=self.investment_option_parser,
            scheme_name_parser=self.scheme_name_parser,
            confidence_parser=self.confidence_parser,
            limit_parser=self.limit_parser
        )

        self.mapper = SchemeMapper()
        self.resolver = SchemeResolver()

        self.service = SchemeService(
            scheme_gateway=scheme_gateway,
            scheme_mapper=self.mapper,
            scheme_query_parser=self.query_parser,
            scheme_resolver=self.resolver
        )

        self.definition = ToolDefinition(
            name=ToolType.SCHEME.value,
            description="Retrieve, compare and recommend mutual fund schemes.",
            capability=Capability.SCHEME,
            timeout_seconds=30,
            tags=[
                "scheme",
                "comparision",
                "nav",
                "returns",
                "holdings"
            ]
        )

        self.tool = SchemeTool(
            scheme_service=self.service
        )