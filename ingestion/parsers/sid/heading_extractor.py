import re

from ingestion.models import ParsedDocument, SectionMarker
from .constants import TOC_ENTRY_END_PATTERN, HEADING_PATTERNS, MIN_HEADING_LENGTH

class SIDHeadingExtractor:

    def extract(self, document: ParsedDocument, skip_until_page: int | None = None) -> list[SectionMarker]:
        markers: list[SectionMarker] = []

        for page in document.pages:
            if skip_until_page is not None and page.page_number <=skip_until_page:
                continue

            lines = page.content.splitlines()

            for line_number, line in enumerate(lines):
                line = line.strip()

                if not line:
                    continue

                # Ignore TOC style lines
                if TOC_ENTRY_END_PATTERN.search(line):
                    continue

                title = self._extract_heading(line)

                if not title:
                    continue

                markers.append(
                    SectionMarker(
                        title=title,
                        page_number=page.page_number,
                        line_number=line_number,
                    )
                )

        return markers

    def _extract_heading(self, line: str) -> str | None:
        for pattern in self.HEADING_PATTERNS:
            match = pattern.match(line)

            if not match:
                continue

            if len(match.groups()) == 2:
                title = match.group(2)
            else:
                title = match.group(1)

            title = self._clean_heading(title)

            if not title:
                return None

            return title

        return None

    def _clean_heading(self, heading: str) -> str | None:
        heading = heading.strip()
        heading = re.sub(r"\s+"," ",heading)

        heading = heading.strip(" .:-")

        if len(heading) < MIN_HEADING_LENGTH:
            return None

        return heading