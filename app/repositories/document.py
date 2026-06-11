from sqlalchemy.orm import Session
from app.models import Document

class DocumentRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, document: Document) -> Document:
        self.db.add(document)
        self.db.flush()
        return document
    
    def get_by_scheme_and_type(
        self,
        scheme_code: str,
        document_type: str
    ):
        return(
            self.db.query(Document)
            .filter(
                Document.scheme_code == scheme_code,
                Document.document_type == document_type

            )
            .first()
        )

