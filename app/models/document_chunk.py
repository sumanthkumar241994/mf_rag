import uuid

from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import VersionChunkMapping


class DocumentChunk(Base):
    __tablename__ = 'document_chunks'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    chunk_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    token_count: Mapped[int] = mapped_column(Integer)
    embedding_model: Mapped[str] = mapped_column(String(255))
    embedding = mapped_column(Vector(1024))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    version_mappings: Mapped[list["VersionChunkMapping"]] = relationship("VersionChunkMapping", back_populates="chunk")


