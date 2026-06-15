from sqlalchemy.orm import Session
from app.models import VersionChunkMapping

class VersionChunkMappingRepository:

    def __init__(self, db: Session) -> None:
        self.db = db
    
    def create(
        self,
        *,
        document_version_id: int,
        chunk_id: int,
        chunk_order: int,
        page_number: int,
        section_title: str,
    ) -> VersionChunkMapping:

        mapping = VersionChunkMapping(
            document_version_id=document_version_id,
            chunk_id=chunk_id,
            chunk_order=chunk_order,
            page_no=page_number,
            section_name=section_title,
        )

        self.db.add(mapping)

        return mapping