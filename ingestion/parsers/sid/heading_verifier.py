from rapidfuzz import fuzz

from ingestion.models import SectionMarker
from .constants import FUZZ_MIN_CONFIDENCE


class SIDHeadingVerifier:
    def verify(self, toc_titles: list[str], markers: list[SectionMarker]) -> list[SectionMarker]:
        if not toc_titles:
            return markers

        best_matches: dict[ str, tuple[int, SectionMarker]] = {}

        for toc_title in toc_titles:
            normalized_toc = self._normalize(toc_title)

            best_score = 0
            best_marker = None

            for marker in markers:
                score = fuzz.token_sort_ratio( 
                    normalized_toc,
                    self._normalize(marker.title),
                )

                if score > best_score:
                    best_score = score
                    best_marker = marker

            if best_marker and best_score >=FUZZ_MIN_CONFIDENCE:
                existing = best_matches.get(normalized_toc)

                if existing is None or best_score > existing[0]:
                    best_matches[normalized_toc] = (
                        best_score,
                        SectionMarker(
                            title=toc_title,
                            page_number=best_marker.page_number,
                            line_number=best_marker.line_number,
                        ),
                    )

        verified_markers = [value[1] for value in best_matches.values()]
        verified_markers.sort( key=lambda marker: (marker.page_number,marker.line_number))
        return verified_markers
        

    def _normalize(self, text: str) -> str:
        text = text.upper()
        text = (
            text
            .replace("?", "")
            .replace(":", "")
            .replace(".", "")
            .replace(",", "")
        )
        text = " ".join(text.split())

        return text