import uuid
from sqlalchemy.orm import Session
from app.models import DocumentVersion

class DocumentVersionRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        document_id: int,
        version_number: int,
        file_name: str,
        file_hash: str,
        s3_path: str,
        is_active: bool = True,
    ) -> DocumentVersion:

        version = DocumentVersion(
            document_id=document_id,
            version_number=version_number,
            file_name=file_name,
            file_hash=file_hash,
            s3_path=s3_path,
            is_active=is_active,
        )

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

    def get_latest_version(self, document_id: uuid.UUID):
        return (
            self.db.query(DocumentVersion)
            .filter(
                DocumentVersion.document_id == document_id,
                DocumentVersion.is_active.is_(True)
            )
            .first()
        )


