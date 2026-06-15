from sqlalchemy.orm import Session
from app.models import Document

class DocumentRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        amc_name: str,
        scheme_name: str,
        document_type: str,
        scheme_code: str | None = None,
    ) -> Document:

        document = Document(
            amc_name=amc_name,
            scheme_name=scheme_name,
            document_type=document_type,
            scheme_code=scheme_code,
        )

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

