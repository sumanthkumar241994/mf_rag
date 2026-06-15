import re
from collections import Counter

from ingestion.models.parsed_document import ParsedDocument
from .models import DocumentLayout

class LayoutDetector:
    TOP_LINES = 3
    BOTTOM_LINES = 3
    MIN_PAGE_RATIO = 0.30
    PAGE_NUMBER_PATTERN = re.compile(r"\b\d+\b")

    def detect(self, document: ParsedDocument) -> DocumentLayout:
        header_counter = Counter()
        footer_counter = Counter()

        total_pages = len(document.pages)

        for page in document.pages:
            lines = [ line.strip() for line in page.content.splitlines() if line.strip()]
            headers = lines[:self.TOP_LINES]
            footers = lines[-self.BOTTOM_LINES:]

            for line in headers:
                header_counter[self._normalize(line)] += 1
            
            for line in footers:
                footer_counter[self._normalize(line)] += 1
            
        threshold = max(2, int(total_pages*self.MIN_PAGE_RATIO))

        return DocumentLayout(
            headers={line for line, count in header_counter.items() if count >=threshold},
            footers= {line for line, count in footer_counter.items() if count >=threshold}
        )
    
    def _normalize(self, line: str) -> str:
        line = self.PAGE_NUMBER_PATTERN.sub("", line)
        line = " ".join(line.split())

        return line.strip()

