from collections.abc import Iterator
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.dependencies import get_db, get_redis
from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# /health/live
# ---------------------------------------------------------------------------


def test_liveness() -> None:
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "environment" in data
    assert "version" in data


# ---------------------------------------------------------------------------
# /health/db
# ---------------------------------------------------------------------------


def test_db_health_ok() -> None:
    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"


def test_db_health_degraded() -> None:
    def broken_get_db() -> Iterator[MagicMock]:
        session = MagicMock()
        session.execute.side_effect = Exception("Connection refused")
        yield session

    app.dependency_overrides[get_db] = broken_get_db
    response = client.get("/api/v1/health/db")
    app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "degraded"
    assert "error" in data["database"]


# ---------------------------------------------------------------------------
# /health/redis
# ---------------------------------------------------------------------------


def test_redis_health_ok() -> None:
    response = client.get("/api/v1/health/redis")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["redis"] == "ok"


def test_redis_health_degraded() -> None:
    def broken_get_redis() -> Iterator[MagicMock]:
        redis = MagicMock()
        redis.ping.side_effect = Exception("Connection refused")
        yield redis

    app.dependency_overrides[get_redis] = broken_get_redis
    response = client.get("/api/v1/health/redis")
    app.dependency_overrides.pop(get_redis, None)

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "degraded"
    assert "error" in data["redis"]


# ---------------------------------------------------------------------------
# /health/  (overall)
# ---------------------------------------------------------------------------


def test_overall_health_ok() -> None:
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"
    assert data["redis"] == "ok"


def test_overall_health_db_degraded() -> None:
    def broken_get_db() -> Iterator[MagicMock]:
        session = MagicMock()
        session.execute.side_effect = Exception("Connection refused")
        yield session

    app.dependency_overrides[get_db] = broken_get_db
    response = client.get("/api/v1/health/")
    app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "degraded"
    assert "error" in data["database"]
    assert data["redis"] == "ok"


def test_overall_health_redis_degraded() -> None:
    def broken_get_redis() -> Iterator[MagicMock]:
        redis = MagicMock()
        redis.ping.side_effect = Exception("Connection refused")
        yield redis

    app.dependency_overrides[get_redis] = broken_get_redis
    response = client.get("/api/v1/health/")
    app.dependency_overrides.pop(get_redis, None)

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "degraded"
    assert data["database"] == "ok"
    assert "error" in data["redis"]
