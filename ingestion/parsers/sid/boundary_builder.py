from re import S

from fastapi._compat.v2 import normalize_name
from ingestion.models import SectionBoundary, SectionMarker

class SIDSectionBoundaryBuilder:

    def build(self, total_pages: int, markers: list[SectionMarker]) -> list[SectionBoundary]:
        boundaries: list[SectionBoundary] = []

        ordered_markers = sorted(markers, key= lambda x:x.page_number)

        for index, marker in enumerate(ordered_markers):
            start_page = marker.page_number

            if index < len(ordered_markers) - 1:
                end_page = (
                    ordered_markers[index+1].page_number-1
                )
            else:
                end_page= total_pages

            boundaries.append(
                SectionBoundary(
                    title=marker.title,
                    normalized_title="",
                    start_page=start_page,
                    end_page=end_page
                )
            )
        
        return boundaries