from rapidfuzz import fuzz

from ingestion.models.section_marker import SectionMarker


class SIDHeadingVerifier:

    MIN_CONFIDENCE = 85

    def verify(
        self,
        toc_titles: list[str],
        markers: list[SectionMarker],
    ) -> list[SectionMarker]:

        if not toc_titles:
            return markers

        verified_markers: list[SectionMarker] = []

        for marker in markers:

            best_match_score = 0

            best_toc_title = None

            for toc_title in toc_titles:

                score = fuzz.token_sort_ratio(
                    self._normalize(marker.title),
                    self._normalize(toc_title),
                )

                if score > best_match_score:
                    best_match_score = score
                    best_toc_title = toc_title

            if best_match_score < self.MIN_CONFIDENCE:
                continue

            verified_markers.append(
                SectionMarker(
                    title=best_toc_title,
                    page_number=marker.page_number,
                    line_number=marker.line_number,
                )
            )

        return verified_markers

    def _normalize(
        self,
        text: str,
    ) -> str:

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