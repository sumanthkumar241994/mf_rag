import uuid

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import DocumentVersion, DocumentChunk

class VersionChunkMapping(Base):
    __tablename__ = 'version_chunk_mappings'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    document_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document_versions.id"))
    document_version: Mapped["DocumentVersion"] = relationship("DocumentVersion", back_populates="chunk_mappings")
    chunk: Mapped["DocumentChunk"] = relationship("DocumentChunk",back_populates="version_mappings")
    chunk_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document_chunks.id"))
    chunk_order: Mapped[int] = mapped_column(Integer)
    page_no: Mapped[int] = mapped_column(Integer, nullable=True)
    section_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())