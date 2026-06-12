import re
from ingestion.contracts import TOCExtractor
from ingestion.models import ParsedDocument, SectionMarker

class SIDTOCExractor(TOCExtractor):
    TOC_PAGE_SCAN_LIMIT = 15
    TOC_REGEX = re.compile(r"([A-Za-z0-9\s\-\&\/\(\)\.,]+?)\s+(\d+)$")
    
    def extract(self, document: ParsedDocument) -> list[SectionMarker]:
        markers: list[SectionMarker] = []

        for page in document.pages[:self.TOC_PAGE_SCAN_LIMIT]:

            for line in page.content.splitlines():
                match = self.TOC_REGEX.search(line.strip())

                if not match:
                    continue

                title = match.group(1).strip()
                page_number = int(match.group(2).strip())

                markers.append(
                    SectionMarker(
                        title=title,
                        page_number=page_number
                    )
                )

        return markers
