import re

SECTION_MAPPING = {
    "investment objective": "INVESTMENT_OBJECTIVE",
    "asset allocation pattern": "ASSET_ALLOCATION",
    "risk factors": "RISK_PROFILE",
    "riskometer": "RISK_PROFILE",
    "investment strategy": "INVESTMENT_STRATEGY",
    "benchmark": "BENCHMARK",
    "fund manager": "FUND_MANAGER",
    "expense ratio": "EXPENSE_RATIO"
}


def semantic_chunk(pages):
    chunks = []

    current_section = "GENERAL"
    current_text = []
    current_page = 1

    for page in pages:
        page_number = page["page_number"]

        lines = page["text"].split("\n")

        for line in lines:
            clean_line = line.strip()

            if not clean_line:
                continue

            section_found = False

            for heading in SECTION_MAPPING:

                if clean_line.lower() == heading:

                    if current_text:
                        chunks.append({
                            "section_name": current_section,
                            "semantic_type": SECTION_MAPPING.get(
                                current_section.lower(),
                                "GENERAL"
                            ),
                            "page_number": current_page,
                            "chunk_text": "\n".join(current_text)
                        })

                    current_section = clean_line
                    current_page = page_number
                    current_text = []

                    section_found = True
                    break

            if not section_found:
                current_text.append(clean_line)

    if current_text:
        chunks.append({
            "section_name": current_section,
            "semantic_type": SECTION_MAPPING.get(
                current_section.lower(),
                "GENERAL"
            ),
            "page_number": current_page,
            "chunk_text": "\n".join(current_text)
        })

    return chunks