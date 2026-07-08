from abc import ABC, abstractmethod

from app.business.scheme.enums.lookup_type import LookupType
from app.business.scheme.parser.lookup_provider import LookupProvider
from app.business.scheme.parser.parser_context import ParserContext


class BaseParser(ABC):

    def __init__(self, lookup_provider: LookupProvider | None = None):
        self.lookup_provider = lookup_provider
    
    @abstractmethod
    def parse(self, context: ParserContext):
        raise NotImplementedError
    
    def find_lookup_match(self, lookup_type: LookupType, query: str) -> tuple[str, str] | None:
        """
        Finds the first matching lookup entry.

        Returns:
            (matched_keyword, canonical_value)
        """
        lookups = self.lookup_provider.lookup(lookup_type)

        # Longest keyword first
        for keyword in sorted(
            lookups.keys(),
            key=len,
            reverse=True,
        ):
            if keyword in query:
                return keyword, lookups[keyword]

        return None