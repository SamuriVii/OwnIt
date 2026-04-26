from collections.abc import AsyncIterator, Generator, Iterator

import pytest
from httpx import ASGITransport, AsyncClient
from loguru import logger
from redis import Redis as RedisClient
from redis.asyncio import Redis as AsyncRedisClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

import app.models  # noqa: F401 # type: ignore
from alembic import command
from alembic.config import Config
from app.api.dependencies import get_async_db, get_async_redis, get_db, get_redis
from app.core.config import settings
from app.main import app as fastapi_app

# ---------------------------------------------------------------------------
# PostgreSQL — Sync (Alembic only)
# ---------------------------------------------------------------------------

engine = create_engine(str(settings.TEST_DB_URL))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def apply_migrations() -> Iterator[None]:
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", str(settings.TEST_DB_URL))
    command.upgrade(config, "head")
    yield


@pytest.fixture
def db_session() -> Iterator[Session]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def override_get_db(db_session: Session) -> Iterator[None]:
    def _get_test_db() -> Iterator[Session]:
        try:
            yield db_session
        finally:
            pass

    fastapi_app.dependency_overrides[get_db] = _get_test_db
    yield
    fastapi_app.dependency_overrides.pop(get_db, None)


# ---------------------------------------------------------------------------
# PostgreSQL — Async (application)
# ---------------------------------------------------------------------------

async_test_engine = create_async_engine(settings.ASYNC_TEST_DB_URL, poolclass=NullPool)


@pytest.fixture
async def async_db_session() -> AsyncIterator[AsyncSession]:
    async with async_test_engine.connect() as conn:
        await conn.begin()
        session = AsyncSession(
            bind=conn, expire_on_commit=False, join_transaction_mode="rollback_only"
        )

        yield session

        await session.close()
        # Redis has no transactions — flushdb() is the only isolation mechanism
        await conn.rollback()


@pytest.fixture(autouse=True)
async def override_get_async_db(async_db_session: AsyncSession) -> AsyncIterator[None]:
    async def _get_test_async_db() -> AsyncIterator[AsyncSession]:
        yield async_db_session

    fastapi_app.dependency_overrides[get_async_db] = _get_test_async_db
    yield
    fastapi_app.dependency_overrides.pop(get_async_db, None)


# ---------------------------------------------------------------------------
# Redis — Sync
# ---------------------------------------------------------------------------


@pytest.fixture
def redis_client() -> Iterator[RedisClient]:
    client: RedisClient = RedisClient.from_url(  # pyright: ignore[reportUnknownMemberType]
        settings.REDIS_TEST_URL, decode_responses=True
    )
    client.flushdb()  # pyright: ignore[reportUnknownMemberType]
    yield client
    client.flushdb()  # pyright: ignore[reportUnknownMemberType]
    client.close()


@pytest.fixture(autouse=True)
def override_get_redis(redis_client: RedisClient) -> Iterator[None]:
    def _get_test_redis() -> Iterator[RedisClient]:
        try:
            yield redis_client
        finally:
            pass

    fastapi_app.dependency_overrides[get_redis] = _get_test_redis
    yield
    fastapi_app.dependency_overrides.pop(get_redis, None)


# ---------------------------------------------------------------------------
# Redis — Async (application)
# ---------------------------------------------------------------------------


@pytest.fixture
async def async_redis_client() -> AsyncIterator[AsyncRedisClient]:
    client: AsyncRedisClient = AsyncRedisClient.from_url(  # pyright: ignore[reportUnknownMemberType]
        settings.REDIS_TEST_URL, decode_responses=True
    )
    await client.flushdb()  # pyright: ignore[reportUnknownMemberType]
    yield client
    await client.flushdb()  # pyright: ignore[reportUnknownMemberType]
    await client.aclose()


@pytest.fixture(autouse=True)
async def override_get_async_redis(
    async_redis_client: AsyncRedisClient,
) -> AsyncIterator[None]:
    async def _get_test_async_redis() -> AsyncIterator[AsyncRedisClient]:
        yield async_redis_client

    fastapi_app.dependency_overrides[get_async_redis] = _get_test_async_redis
    yield
    fastapi_app.dependency_overrides.pop(get_async_redis, None)


# ---------------------------------------------------------------------------
# HTTP Client
# ---------------------------------------------------------------------------


@pytest.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),  # type: ignore[arg-type]
        base_url="http://test",
    ) as client:
        yield client


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


@pytest.fixture
def caplog_loguru(
    caplog: pytest.LogCaptureFixture,
) -> Generator[pytest.LogCaptureFixture, None, None]:
    handler_id: int = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=True,  # thread-safe for async tests
    )
    yield caplog
    logger.remove(handler_id)
