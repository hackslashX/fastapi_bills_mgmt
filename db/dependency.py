from sqlalchemy.ext.asyncio import AsyncSession

from instance.config import config

from .session import AsyncSessionMaker


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    db: AsyncSession = AsyncSessionMaker()
    try:
        db.sync_session.set_bind_key(config.DB_BIND)
        yield db
    finally:
        await db.close()
