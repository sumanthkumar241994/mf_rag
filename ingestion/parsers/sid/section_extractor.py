from ingestion.models import DocumentSection, ParsedDocument, SectionBoundary
from .constants import PAGE_NUMBER_PATTERNS

class SIDSectionExtractor:
    def extract(self, document: ParsedDocument, boundaries: list[SectionBoundary]) -> list[DocumentSection]:
        sections: list[DocumentSection] = []
        page_map = {page.page_number: page for page in document.pages}

        for boundary in boundaries:
            content_parts: list[str] = []
            for page_number in range(boundary.start_page, boundary.end_page + 1):
                page = page_map.get(page_number)

                if not page:
                    continue

                lines = page.content.splitlines()
                selected_lines = self._extract_lines(lines=lines, page_number=page_number, boundary=boundary)
                selected_lines = self._clean_lines(selected_lines)
                content_parts.extend(selected_lines)

            content = "\n".join(content_parts).strip()

            sections.append(
                DocumentSection(
                    title=boundary.title,
                    content=content,
                    page_number=boundary.start_page,
                )
            )

        return sections
    
    def _extract_lines(self, lines: list[str], page_number: int, boundary: SectionBoundary) -> list[str]:
        # Same page
        if boundary.start_page == boundary.end_page == page_number:
            return lines[boundary.start_line : boundary.end_line + 1]
        # Start page
        if page_number == boundary.start_page:
            return lines[boundary.start_line :]
        # End page
        if page_number == boundary.end_page:
            return lines[ : boundary.end_line + 1]
        # Middle page
        return lines

    def _clean_lines(self, lines: list[str]) -> list[str]:
        cleaned = []
        for line in lines:
            line = line.strip()

            if not line:
                continue

            if PAGE_NUMBER_PATTERNS.match(line):
                continue

            cleaned.append(line)

        return cleaned
