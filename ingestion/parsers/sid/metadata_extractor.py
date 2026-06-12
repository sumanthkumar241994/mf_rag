import re

from ingestion.models import ParsedDocument

class SIDMetaDataExtractor:
    def extract(self, document: ParsedDocument) -> dict:
        text = "\n".join(page.content for page in document.pages[:5])

        return {
            "amc_name": self._extract_amc(text),
            "scheme_name": self._extract_scheme(text),
            "scheme_category": self._extract_category(text)
        }

    def _extract_amc(self, text):
        return ""

    def _extract_scheme(self, text):
        return ""

    def _extract_category(self, text):
        return ""