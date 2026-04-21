from redis.client import Redis
from redis.connection import ConnectionPool

from app.core.config import settings

redis_pool = ConnectionPool.from_url(  # pyright: ignore[reportUnknownMemberType]
    settings.REDIS_URL,
    max_connections=settings.REDIS_MAX_CONNECTIONS,
    decode_responses=True,
)


def get_redis_client() -> Redis:
    return Redis(connection_pool=redis_pool)
