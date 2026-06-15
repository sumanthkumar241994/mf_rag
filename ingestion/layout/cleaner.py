import re

from ingestion.layout.models import DocumentLayout


class LayoutCleaner:
    PAGE_NUMBER_PATTERN = re.compile(r"\b\d+\b")

    def clean(self, content: str, layout: DocumentLayout) -> str:
        cleaned = []

        for line in content.splitlines():
            normalized = self._normalize(line)

            if normalized in layout.headers:
                continue

            if normalized in layout.footers:
                continue

            cleaned.append(line)

        return "\n".join(cleaned)
    
    def _normalize(self, line: str) -> str:
        line = self.PAGE_NUMBER_PATTERN.sub("", line)
        line = " ".join(line.split())

        return line.strip()
