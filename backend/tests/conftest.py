from collections.abc import Generator, Iterator

import pytest
from loguru import logger
from redis import Redis as RedisClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import app.models  # noqa: F401 # type: ignore
from alembic import command
from alembic.config import Config
from app.api.dependencies import get_db, get_redis
from app.core.config import settings
from app.main import app as fastapi_app

# ---------------------------------------------------------------------------
# PostgreSQL
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
# Redis
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
