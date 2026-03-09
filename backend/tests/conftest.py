from collections.abc import Generator, Iterator

import pytest
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import app.models  # noqa: F401 # type: ignore
from alembic import command
from alembic.config import Config
from app.api.dependencies import get_db
from app.core.config import settings
from app.main import app as fastapi_app

# Setup the test database engine and session factory
engine = create_engine(str(settings.TEST_DB_URL))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def apply_migrations() -> Iterator[None]:
    """
    Applies Alembic migrations to the test database at the start of the test session.
    This ensures the schema is always up-to-date with the latest code changes.
    """
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", str(settings.TEST_DB_URL))

    # Run migrations to 'head'
    command.upgrade(config, "head")

    yield

    # Optional: You can drop everything here if you want a clean state for next time
    # Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Iterator[Session]:
    """
    Provides a clean, transactional database session for each test.
    Rolls back any changes after the test is completed to ensure isolation.
    """
    connection = engine.connect()
    # Begin a nested transaction
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    # Close session and rollback all changes made during the test
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def override_get_db(db_session: Session) -> Iterator[None]:
    """
    Overrides the 'get_db' dependency in FastAPI with our test session.
    The 'autouse=True' ensures every request during testing uses the test database.
    """

    def _get_test_db() -> Iterator[Session]:
        try:
            yield db_session
        finally:
            pass

    # Inject the override
    fastapi_app.dependency_overrides[get_db] = _get_test_db

    yield

    # Clean up the override after the test finishes
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def caplog_loguru(
    caplog: pytest.LogCaptureFixture,
) -> Generator[pytest.LogCaptureFixture, None, None]:
    """
    Redirects Loguru logs to the standard Pytest caplog handler.
    Allows for asserting log messages in tests using 'assert message in caplog.text'.
    """
    # Add the Pytest caplog handler to Loguru
    handler_id: int = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=True,  # Ensure thread-safety for async tests
    )
    yield caplog

    # Remove the handler after the test to prevent log leakage between tests
    logger.remove(handler_id)
