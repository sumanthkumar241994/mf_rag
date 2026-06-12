from ingestion.models import DocumentSection, ParsedDocument, SectionBoundary

class SIDSectionExtractor:
    def extract(
        self, 
        document: ParsedDocument, 
        boundaries: list[SectionBoundary]
        ) -> list[DocumentSection]:

        sections: list[DocumentSection] = []

        page_map = {
            page.page_number: page.content for page in document.pages
        }

        for boundary in boundaries:
            content_parts: list[str] = []

            for page_no in range(boundary.start_page, boundary.end_page+1):
                content = page_map.get(page_no, "")

                content_parts.append(content)
            
            sections.append(
                DocumentSection(
                    title=boundary.title,
                    content='\n'.join(content_parts),
                    page_number=boundary.start_page
                )
            )

        return sections
