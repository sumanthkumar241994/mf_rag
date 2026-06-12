from ingestion.models import Page
from ingestion.exceptions import CorruptedPDFException, PasswordProtectedPDFException
import fitz

class PDFTextExtractor:

    def extract(self, file_path: str) -> list[Page]:
        pdf = fitz.open(file_path)

        if pdf.needs_pass:
            raise PasswordProtectedPDFException(file_path)
            
        pages: list[Page] = []

        try:
            for page_index in range(len(pdf)):
                page = pdf.load_page(page_index)
                content = page.get_text("text")

                pages.append(
                    Page(
                        page_number=page_index + 1,
                        content=content,
                        char_count=len(content)
                    )
                )
            
            return pages
        except Exception as ex:
            raise CorruptedPDFException(file_path) from ex
        
        finally:
            pdf.close()


