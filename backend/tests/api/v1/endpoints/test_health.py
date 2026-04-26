from collections.abc import AsyncIterator
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from app.api.dependencies import get_async_db, get_async_redis
from app.main import app

# ---------------------------------------------------------------------------
# /health/live
# ---------------------------------------------------------------------------


async def test_liveness(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "environment" in data
    assert "version" in data


# ---------------------------------------------------------------------------
# /health/db
# ---------------------------------------------------------------------------


async def test_db_health_ok(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/health/db")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"


async def test_db_health_degraded(async_client: AsyncClient) -> None:
    async def broken_get_async_db() -> AsyncIterator[MagicMock]:
        session = MagicMock()
        session.execute = AsyncMock(side_effect=Exception("Connection refused"))
        yield session

    app.dependency_overrides[get_async_db] = broken_get_async_db
    response = await async_client.get("/api/v1/health/db")
    app.dependency_overrides.pop(get_async_db, None)

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "degraded"
    assert "error" in data["database"]


# ---------------------------------------------------------------------------
# /health/redis
# ---------------------------------------------------------------------------


async def test_redis_health_ok(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/health/redis")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["redis"] == "ok"


async def test_redis_health_degraded(async_client: AsyncClient) -> None:
    async def broken_get_async_redis() -> AsyncIterator[MagicMock]:
        redis = MagicMock()
        redis.ping = AsyncMock(side_effect=Exception("Connection refused"))
        yield redis

    app.dependency_overrides[get_async_redis] = broken_get_async_redis
    response = await async_client.get("/api/v1/health/redis")
    app.dependency_overrides.pop(get_async_redis, None)

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "degraded"
    assert "error" in data["redis"]


# ---------------------------------------------------------------------------
# /health/  (overall)
# ---------------------------------------------------------------------------


async def test_overall_health_ok(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"
    assert data["redis"] == "ok"


async def test_overall_health_db_degraded(async_client: AsyncClient) -> None:
    async def broken_get_async_db() -> AsyncIterator[MagicMock]:
        session = MagicMock()
        session.execute = AsyncMock(side_effect=Exception("Connection refused"))
        yield session

    app.dependency_overrides[get_async_db] = broken_get_async_db
    response = await async_client.get("/api/v1/health/")
    app.dependency_overrides.pop(get_async_db, None)

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "degraded"
    assert "error" in data["database"]
    assert data["redis"] == "ok"


async def test_overall_health_redis_degraded(async_client: AsyncClient) -> None:
    async def broken_get_async_redis() -> AsyncIterator[MagicMock]:
        redis = MagicMock()
        redis.ping = AsyncMock(side_effect=Exception("Connection refused"))
        yield redis

    app.dependency_overrides[get_async_redis] = broken_get_async_redis
    response = await async_client.get("/api/v1/health/")
    app.dependency_overrides.pop(get_async_redis, None)

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "degraded"
    assert data["database"] == "ok"
    assert "error" in data["redis"]


# ---------------------------------------------------------------------------
# Marker — remove if pytest-asyncio asyncio_mode = "auto" is set
# ---------------------------------------------------------------------------

pytestmark = pytest.mark.asyncio
