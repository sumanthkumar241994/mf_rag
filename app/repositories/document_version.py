import uuid
from sqlalchemy.orm import Session
from app.models import DocumentVersion

class DocumentVersionRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, version: DocumentVersion) -> DocumentVersion:
        self.db.add(version)
        self.db.flush()
        return version

    def deactivate_version(self, document_id: uuid.UUID, version_no):
        (
            self.db.query(DocumentVersion)
            .filter(
                DocumentVersion.document_id == document_id,
                DocumentVersion.version_no == version_no
            )
            .update(
                {"is_active": False}
            )
        )

    def get_active_version(self, document_id: uuid.UUID):
        return (
            self.db.query(DocumentVersion)
            .filter(
                DocumentVersion.document_id == document_id,
                DocumentVersion.is_active.is_(True)
            )
            .first()
        )


