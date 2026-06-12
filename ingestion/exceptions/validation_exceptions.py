from .base import IngestionException

class PDFValidationException(IngestionException):
    """
    Base exception for pdf validation failures
    """

class EmptyPDFException(PDFValidationException):
    def __init__(self) -> None:
        super().__init__(
            message='No pages extracted from the PDF', 
            error_code='EMPTY_PDF'
            )


class NoTextExtractedException(PDFValidationException):
    """
    Raised when text extraction returns empty content.
    """

    def __init__(self) -> None:
        super().__init__(
            message="No text could be extracted from PDF",
            error_code="NO_TEXT_EXTRACTED",
        )


class ScannedPDFException(PDFValidationException):
    """
    Raised when the PDF appears to be scanned
    and contains little or no machine-readable text.
    """

    def __init__(self) -> None:
        super().__init__(
            message="Scanned PDF detected",
            error_code="SCANNED_PDF",
        )


class InsufficientTextException(PDFValidationException):
    """
    Raised when extracted text volume is below threshold.
    """

    def __init__(
        self,
        actual_chars: int,
        minimum_chars: int,
    ) -> None:
        super().__init__(
            message=(
                f"Extracted text too small. "
                f"Expected >= {minimum_chars}, "
                f"received {actual_chars}"
            ),
            error_code="INSUFFICIENT_TEXT",
        )