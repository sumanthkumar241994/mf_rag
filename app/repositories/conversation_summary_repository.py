from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation_summary import ConversationSummary


class ConversationSummaryRepository:
    """
    Repository responsible for conversation summary persistence.

    Responsibilities:
    - Store generated summaries
    - Retrieve latest summary
    - Retrieve summary history

    No business logic should exist in this layer.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, summary: ConversationSummary) -> ConversationSummary:
        self.db.add(summary)
        await self.db.flush()
        await self.db.refresh(summary)

        return summary

    async def get_by_id(self, summary_id: UUID) -> Optional[ConversationSummary]:
        stmt = (
            select(ConversationSummary)
            .where(
                ConversationSummary.id == summary_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_latest(self, conversation_id: UUID) -> Optional[ConversationSummary]:
        stmt = (
            select(ConversationSummary)
            .where(
                ConversationSummary.conversation_id == conversation_id
            )
            .order_by(
                ConversationSummary.version.desc()
            )
            .limit(1)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_latest_version(self, conversation_id: UUID) -> int:
        stmt = (
            select(
                func.max(
                    ConversationSummary.version
                )
            )
            .where(
                ConversationSummary.conversation_id == conversation_id
            )
        )

        result = await self.db.execute(stmt)

        version = result.scalar_one()

        return version or 0

    async def get_latest_sequence(self,conversation_id: UUID) -> int:
        stmt = (
            select(
                func.max(
                    ConversationSummary.end_sequence
                )
            )
            .where(
                ConversationSummary.conversation_id == conversation_id
            )
        )

        result = await self.db.execute(stmt)

        sequence = result.scalar_one()

        return sequence or 0

    async def get_all(self,conversation_id: UUID) -> list[ConversationSummary]:
        stmt = (
            select(ConversationSummary)
            .where(
                ConversationSummary.conversation_id == conversation_id
            )
            .order_by(
                ConversationSummary.version
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def exists(
        self,
        conversation_id: UUID,
        version: int,
    ) -> bool:
        stmt = (
            select(ConversationSummary.id)
            .where(
                ConversationSummary.conversation_id == conversation_id,
                ConversationSummary.version == version,
            )
            .limit(1)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none() is not None