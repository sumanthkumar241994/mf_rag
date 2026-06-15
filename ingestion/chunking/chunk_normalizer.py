import re

class ChunkNormalizer:
    PAGE_NUMBER_PATTERN = re.compile(r"^\d+$")
    SO_PATTERN = re.compile(r"^SO\s+\d+(\s*&\s*\d+)?$")

    def normalize(self, text: str) -> str:
        lines = []

        for line in text.splitlines():
            line = line.strip()

            if not line:
                continue

            if self.PAGE_NUMBER_PATTERN.match(line):
                continue

            if self.SO_PATTERN.match(line):
                continue

            lines.append(line)
        
        normalized = " ".join(lines)
        normalized = re.sub(r"\s+", " ", normalized)
        
        return normalized.strip()

        