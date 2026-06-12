import re

class SchemeNameExtractor:
    SECTION_PATTERN = re.compile(
        r"SECTION\s+I",
        re.IGNORECASE,
    )

    INVALID_LINES = {
        "SECTION I",
        "SCHEME INFORMATION DOCUMENT",
        "KEY INFORMATION MEMORANDUM",
    }

    SCHEME_KEYWORDS = (
        "FUND",
        "SCHEME",
        "ETF",
    )

    def extract(self, text: str) -> str | None:
        lines = self._clean_lines(text)
        scheme_name = self._extract_after_section(lines)

        if scheme_name:
            return scheme_name
        
        return self._fallback_extract(lines)
    

    def _clean_lines(text: str) -> list[str]:
        return [
            line.strip() for line in text.splitlines() if line.strip()
        ]

    def _extract_after_section(self, lines: list[str]) -> str | None:
        for index, line in lines:
            if not self.SECTION_PATTERN.search(line):
                continue

            for next_index in range(index + 1, min(index+10, len(lines))):
                candidate = lines[next_index]

                if self._is_scheme_name(candidate):
                    return candidate
                
            break
        
        return None

        
    def _is_scheme_name(self, text: str) -> bool:
        if not text: 
            return False
        
        text_upper = text.upper()
        return any(
            keyword in text_upper for keyword in self.SCHEME_KEYWORDS
        )
    
    def _fallback_extract(self, lines: list[str]) -> str | None:
        for line in lines:
            if self._is_scheme_name(line):
                    return line
                
        return None


