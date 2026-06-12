from rapidfuzz import fuzz
from ingestion.metadata.constants import AMC_ALIASES

class AMCResolver:
    MIN_SCORE = 90
    def resolve(self, text: str) -> str | None:
        if not text:
            return None

        text = text.upper()

        best_match = None
        best_score = 0

        for amc_name, aliases in AMC_ALIASES.items():
            for alias in aliases:
                score = fuzz.partial_ratio(
                    alias.upper(),
                    text
                )

                if score > best_score:
                    best_score = score
                    best_match = amc_name
        
        if best_score >= self.MIN_SCORE:
            return best_match
        
        return None