from sqlalchemy.orm import Session
from app.models import VersionChunkMapping

class VersionChunkMappingRepository:

    def __init__(self, db: Session) -> None:
        self.db = db
    
    def create(self, mapping: VersionChunkMapping):
        self.db.add(mapping)
        self.db.flush()
        return mapping