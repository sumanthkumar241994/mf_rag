import re

from ingestion.models import ParsedDocument, TOCExtractionResult


from .constants import (MIN_TOC_LINES_PER_PAGE, MULTIPLE_SPACE_PATTERN,
    SECTION_PREFIX_PATTERN, TOC_ENTRY_END_PATTERN,TOC_LINE_PATTERN,
    TOC_SCAN_LIMIT
)


class SIDTOCExtractor:
    def extract(self, document: ParsedDocument) -> TOCExtractionResult:
        toc_titles: list[str] = []
        toc_start_page: int | None = None
        toc_end_page: int | None = None

        for page in document.pages[:TOC_SCAN_LIMIT]:
            toc_entries = self._extract_toc_entries(page.content)

            if  len(toc_entries) < MIN_TOC_LINES_PER_PAGE:
                continue

            if toc_start_page is None:
                toc_start_page = page.page_number

            toc_end_page = page.page_number

            for entry in toc_entries:
                title = self._extract_title(entry)

                if not title:
                    continue

                toc_titles.append(title)

        toc_titles = list(
            dict.fromkeys(toc_titles)
        )

        return TOCExtractionResult(
            found=len(toc_titles) > 0,
            titles=toc_titles,
            toc_start_page=toc_start_page,
            toc_end_page=toc_end_page,
        )
    
    
    def _extract_title(self, entry: str) -> str | None:
        entry = entry.strip()

        if not entry:
            return None

        if not TOC_LINE_PATTERN.match(entry):
            return None

        #Remove: ............. 25
        title = re.sub(r"\.{3,}\s*\d+\s*$","",entry)
        # Remove: A. B. I. II.
        title = SECTION_PREFIX_PATTERN.sub("", title)
        # Collapse whitespace
        title = MULTIPLE_SPACE_PATTERN.sub(" ", title)
        title = title.strip()

        # Ignore noise
        if len(title) < 5:
            return None

        return title

    def _extract_toc_entries(self, content: str) -> list[str]:
        entries: list[str] = []

        lines = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

        current_parts: list[str] = []

        for line in lines:
            current_parts.append(line)

            if TOC_ENTRY_END_PATTERN.search(line):
                entries.append(" ".join(current_parts))
                current_parts = []

        return entries