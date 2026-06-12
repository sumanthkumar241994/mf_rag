from ingestion.models import SectionBoundary, ParsedDocument, SectionMarker

class SIDSectionBoundaryBuilder:

    def build(
        self,
        markers: list[SectionMarker],
        document: ParsedDocument,
    ) -> list[SectionBoundary]:

        boundaries = []

        markers = sorted(
            markers,
            key=lambda m: (
                m.page_number,
                m.line_number,
            ),
        )

        for idx, marker in enumerate(markers):

            if idx < len(markers) - 1:

                next_marker = markers[idx + 1]

                boundaries.append(
                    SectionBoundary(
                        title=marker.title,
                        normalized_title="",
                        start_page=marker.page_number,
                        start_line=marker.line_number,
                        end_page=next_marker.page_number,
                        end_line=next_marker.line_number - 1,
                    )
                )

            else:

                last_page = document.pages[-1]

                boundaries.append(
                    SectionBoundary(
                        title=marker.title,
                        normalized_title="",
                        start_page=marker.page_number,
                        start_line=marker.line_number,
                        end_page=last_page.page_number,
                        end_line=999999,
                    )
                )

        return boundaries