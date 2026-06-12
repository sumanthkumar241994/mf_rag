from ingestion.exceptions.base import IngestionException

class PDFLoadException(IngestionException):
    """
    Raise an exception when pdf is not loaded
    """
    pass

class PDFNotFoundError(PDFLoadException):
    """
    Raise when pdf file does not exist
    """
    def __init__(self,file_path: str) -> None:
        super().__init__(message=f"PDF File not found: {file_path}", error_code='PDF_NOT_FOUND')


class CorruptedPDFException(PDFLoadException):
    """
    Raise when PDF file is corrupted
    """
    def __init__(self, file_path: str) -> None:
        super().__init__(message=f"Corrupted File Detected: {file_path}", error_code='PDF_CORRUPTED')


class PasswordProtectedPDFException(PDFLoadException):
    """
    Raise when pdf file requires password
    """
    def __init__(self, file_path: str) -> None:
        super().__init__(message=f"Password-protected pdf detected: {file_path}", error_code='PDF_PROTECTED')