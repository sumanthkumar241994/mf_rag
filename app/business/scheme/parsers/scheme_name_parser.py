import re
from app.business.scheme.parser.parser_context import ParserContext
from app.business.scheme.parsers.base_parser import BaseParser


class SchemeNameParser(BaseParser):
    SEPARATORS = re.compile(
        r"\s+(?:and|vs)\s+|,",
        re.IGNORECASE
    )

    PARSER_KEYWORDS = [
        "compare",
        "recommend",
        "top",
        "best",
        "show",
        "tell",
        "about",
        "give",
        "analyze",
        "review"
    ]

    def parse(self, context: ParserContext):
        query = context.cleaned_query

        if context.recommendation:
            return

        for word in self.PARSER_KEYWORDS:
            query = re.sub(rf"\b{re.escape(word)}\b", "", query, flags=re.IGNORECASE)

        query = re.sub(r"\s+", " ", query).strip()

        if context.compare:
            names = [
                part.strip()
                for part in self.SEPARATORS.split(query)
                if part.strip()
            ]
            context.scheme_names.append(names)
        else:
            if query:
                context.scheme_names.append(query)
        
        context.matches['scheme_names'] = context.scheme_names