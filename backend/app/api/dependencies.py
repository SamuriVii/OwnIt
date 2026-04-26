from collections.abc import AsyncIterator, Iterator
from typing import Annotated

from fastapi import Depends
from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.database.async_redis import get_async_redis_client
from app.database.async_session import AsyncSessionLocal
from app.database.redis import get_redis_client
from app.database.session import SessionLocal

# ---------------------------------------------------------------------------
# Sync — Alembic / internal use only
# ---------------------------------------------------------------------------


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis() -> Iterator[Redis]:
    client = get_redis_client()
    try:
        yield client
    finally:
        client.close()


# ---------------------------------------------------------------------------
# Async — application
# ---------------------------------------------------------------------------


async def get_async_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_async_redis() -> AsyncIterator[AsyncRedis]:
    client = get_async_redis_client()
    try:
        yield client
    finally:
        await client.aclose()


# ---------------------------------------------------------------------------
# Annotated aliases — use these in endpoint signatures instead of Depends(...)
# ---------------------------------------------------------------------------

AsyncDB = Annotated[AsyncSession, Depends(get_async_db)]
AsyncRedisClient = Annotated[AsyncRedis, Depends(get_async_redis)]
