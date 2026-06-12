import re

from ingestion.models import ParsedDocument


class SIDTOCExtractor:

    TOC_PAGE_SCAN_LIMIT = 15

    TOC_LINE_PATTERN = re.compile(
        r"^(.*?)\s*\.{2,}\s*(\d+)\s*$"
    )

    SECTION_PREFIX_PATTERN = re.compile(
        r"^([A-Z]|[IVXLCDM]+)[\.\)]\s+",
        re.IGNORECASE,
    )

    def extract(
        self,
        document: ParsedDocument,
    ) -> list[str]:

        sections: list[str] = []
        seen: set[str] = set()

        for page in document.pages[: self.TOC_PAGE_SCAN_LIMIT]:

            lines = page.content.splitlines()

            toc_hits = 0

            for line in lines:

                line = line.strip()

                if self.TOC_LINE_PATTERN.search(line):
                    toc_hits += 1

            # probably not a TOC page
            if toc_hits < 3:
                continue

            for line in lines:

                title = self._extract_title(line)

                if not title:
                    continue

                normalized = title.upper()

                if normalized in seen:
                    continue

                seen.add(normalized)

                sections.append(title)

        return sections

    def _extract_title(
        self,
        line: str,
    ) -> str | None:

        line = line.strip()

        if not line:
            return None

        match = self.TOC_LINE_PATTERN.match(line)

        if not match:
            return None

        title = match.group(1)

        # remove roman numerals / A. / B.
        title = self.SECTION_PREFIX_PATTERN.sub(
            "",
            title,
        )

        title = re.sub(
            r"\s+",
            " ",
            title,
        )

        title = title.strip()

        if len(title) < 5:
            return None

        return title