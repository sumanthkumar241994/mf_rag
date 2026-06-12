import re

from ingestion.models import (
    SectionMarker, ParsedDocument
)


class SIDHeadingExtractor:

    HEADING_PATTERNS = [
        re.compile(
            r"^[A-Z]\.\s+(.+)$"
        ),
        re.compile(
            r"^[IVXLCDM]+\.\s+(.+)$"
        ),
    ]

    def extract(
        self,
        document: ParsedDocument,
    ) -> list[SectionMarker]:

        markers = []

        for page in document.pages:

            lines = page.content.splitlines()

            for line_number, line in enumerate(lines):

                line = line.strip()

                if not line:
                    continue

                for pattern in self.HEADING_PATTERNS:

                    match = pattern.match(line)

                    if not match:
                        continue

                    markers.append(
                        SectionMarker(
                            title=match.group(1).strip(),
                            page_number=page.page_number,
                            line_number=line_number,
                        )
                    )

        return markers