from ingestion.models import ParsedDocument, SectionBoundary, DocumentSection

class SIDSectionExtractor:

    def extract(
        self,
        document: ParsedDocument,
        boundaries: list[SectionBoundary],
    ) -> list[DocumentSection]:

        sections = []

        page_map = {
            page.page_number: page
            for page in document.pages
        }

        for boundary in boundaries:

            content_parts = []

            for page_no in range(
                boundary.start_page,
                boundary.end_page + 1,
            ):

                page = page_map[page_no]

                lines = page.content.splitlines()

                if (
                    page_no
                    == boundary.start_page
                    == boundary.end_page
                ):

                    selected_lines = lines[
                        boundary.start_line :
                        boundary.end_line + 1
                    ]

                elif page_no == boundary.start_page:

                    selected_lines = lines[
                        boundary.start_line :
                    ]

                elif page_no == boundary.end_page:

                    selected_lines = lines[
                        : boundary.end_line + 1
                    ]

                else:

                    selected_lines = lines

                content_parts.extend(
                    selected_lines
                )

            sections.append(
                DocumentSection(
                    title=boundary.title,
                    content="\n".join(
                        content_parts
                    ),
                    page_number=boundary.start_page,
                )
            )

        return sections