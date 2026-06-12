from ingestion.models import Page
from ingestion.exceptions import EmptyPDFException, InsufficientTextException

class PDFValidator:
    MIN_CHARACTERS = 100

    def validate(self, pages: list[Page]) -> None:
        
        if not pages:
            raise EmptyPDFException()

        total_chars = sum(page.char_count for page in pages)

        if total_chars < self.MIN_CHARACTERS:
            raise InsufficientTextException(actual_chars=total_chars, minimum_chars=self.MIN_CHARACTERS)
