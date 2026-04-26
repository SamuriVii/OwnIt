from redis.asyncio import ConnectionPool as AsyncConnectionPool
from redis.asyncio import Redis as AsyncRedis

from app.core.config import settings

async_redis_pool = AsyncConnectionPool.from_url(  # pyright: ignore[reportUnknownMemberType]
    settings.REDIS_URL,
    max_connections=settings.REDIS_MAX_CONNECTIONS,
    decode_responses=True,
)


def get_async_redis_client() -> AsyncRedis:
    return AsyncRedis(connection_pool=async_redis_pool)
