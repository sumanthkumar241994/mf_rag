import uuid
from datetime import date
from sqlalchemy import Boolean, String, DateTime, ForeignKey, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Document, VersionChunkMapping


class DocumentVersion(Base):
    __tablename__ = 'document_versions'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id"))
    document: Mapped["Document"] = relationship("Document", back_populates="versions")
    chunk_mappings: Mapped[list["VersionChunkMapping"]] = relationship(
        "VersionChunkMapping", 
        back_populates="document_version", 
        cascade="all, delete-orphan",
    )
    version_no: Mapped[int] = mapped_column(Integer)
    file_name: Mapped[str] = mapped_column(String(511))
    s3_bucket: Mapped[str] = mapped_column(String(255))
    s3_key: Mapped[str] = mapped_column(String)
    file_hash: Mapped[str] = mapped_column(String(64))
    effective_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    uploaded_by: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())



