from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

class DatabaseComposition:

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ):
        self.session_factory = session_factory