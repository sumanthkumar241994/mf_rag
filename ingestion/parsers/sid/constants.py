import re

TOC_SCAN_LIMIT = 15
MIN_TOC_LINES_PER_PAGE = 3
MIN_HEADING_LENGTH = 5
FUZZ_MIN_CONFIDENCE = 85

TOC_ENTRY_END_PATTERN = re.compile(r"\.{3,}\s*\d+\s*$")
TOC_LINE_PATTERN = re.compile(r".+\.{3,}\s*\d+\s*$")
SECTION_PREFIX_PATTERN = re.compile(r"^([A-Z]|[IVXLCDM]+)[\.\)]\s+",re.IGNORECASE)
MULTIPLE_SPACE_PATTERN = re.compile(r"\s+")
HEADING_PATTERNS = [
        # A. HOW WILL THE SCHEME INVEST?
        re.compile(r"^([A-Z])\.\s+(.+)$"),
        # I. BENCHMARK
        re.compile(r"^([IVXLCDM]+)\.\s+(.+)$", re.IGNORECASE),
        # PART I
        re.compile(r"^(PART\s+[IVXLCDM]+.*)$", re.IGNORECASE),
    ]


