import re

class SectionCategoryResolver:
    CATEGORY_MAP = {
        "INVESTMENT OBJECTIVE": "objective",
        "HOW WILL THE SCHEME ALLOCATE ASSETS": "asset_allocation",
        "WHERE WILL THE SCHEME INVEST": "investment_universe",
        "INVESTMENT STRATEGIES": "investment_strategy",
        "WHAT ARE THE INVESTMENT STRATEGIES": "investment_strategy",
        "BENCHMARK": "benchmark",
        "WHO MANAGES THE SCHEME": "fund_manager",
        "RISK FACTORS": "risk",
        "FUNDAMENTAL ATTRIBUTES": "fundamental_attributes",
        "LOAD STRUCTURE": "load_structure",
        "TAXATION": "taxation",
    }

    def resolve(self, section_title: str) -> str:
        normalized = re.sub(r"[^A-Z0-9\s]", "", section_title.upper())
        normalized = re.sub(r"\s+", " ", normalized,).strip()

        for key, category in self.CATEGORY_MAP.items():
            key_normalized = re.sub(r"[^A-Z0-9\s]", "", key.upper())
            if key_normalized in normalized:
                return category

        return "other"