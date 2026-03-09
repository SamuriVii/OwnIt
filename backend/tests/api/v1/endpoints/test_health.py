import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_integrated(caplog_loguru: pytest.LogCaptureFixture) -> None:
    """
    Test if the healthcheck endpoint correctly connects to the test database.
    Added '-> None' return type to satisfy Mypy and Ruff.
    """
    response = client.get("/api/v1/health/")

    # 1. Check HTTP Status
    assert response.status_code == 200

    # 2. Parse JSON response
    data = response.json()

    # 3. Verify the logic
    assert data["status"] == "ok"
    assert data["database"] == "ok"
    assert data["environment"] == "development"
    assert "Health check requested" in caplog_loguru.text
