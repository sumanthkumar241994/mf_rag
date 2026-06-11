import uuid

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import DocumentVersion

class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    fund_house: Mapped[str] = mapped_column(String(100))
    scheme_code: Mapped[str] = mapped_column(String(255), nullable=True)
    scheme_name: Mapped[str] = mapped_column(String(255))
    document_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), default='active')
    versions: Mapped[list["DocumentVersion"]] = relationship('DoumentVersion', back_populates='document', cascade='all, delete-orphan')
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
