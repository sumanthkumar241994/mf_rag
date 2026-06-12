import re
from ingestion.models import ParsedDocument, SectionMarker

class SIDHeadingExtractor:
    HEADING_PATTERN = re.compile(
        r"^([IVXLCDM]+)\.?\s+(.+)$",
        re.IGNORECASE,
    )

    def extract(self, document: ParsedDocument) -> list[SectionMarker]:
        markers : list[SectionMarker] = []

        for page in document.pages:
            for line in page.content.splitlines():
                line = line.strip()

                match = self.HEADING_PATTERN.match(line)

                if not match:
                    continue

                markers.append(
                    SectionMarker(
                        title=match.group(2).strip(),
                        page_number=page.page_number
                    )
                )

        return markers
