from ingestion.models import ParsedDocument, SectionBoundary, SectionMarker


class SectionBoundaryBuilder:
    def build(self, markers: list[SectionMarker], document: ParsedDocument) -> list[SectionBoundary]:
        if not markers:
            return []

        markers = sorted(markers,key=lambda marker: (marker.page_number,marker.line_number))
        boundaries: list[SectionBoundary] = []

        for index, marker in enumerate(markers):
            start_page = marker.page_number
            start_line = marker.line_number

            if index < len(markers) - 1:
                next_marker = markers[index + 1]
                end_page = next_marker.page_number
                end_line = next_marker.line_number - 1

                # Same page edge case
                if  end_page == start_page and end_line < start_line:
                    end_line = start_line

            else:
                last_page = document.pages[-1]
                end_page = last_page.page_number
                end_line = len(last_page.content.splitlines()) - 1

            boundaries.append(
                SectionBoundary(
                    title=marker.title,
                    start_page=start_page,
                    start_line=start_line,
                    end_page=end_page,
                    end_line=end_line,
                )
            )

        return boundaries