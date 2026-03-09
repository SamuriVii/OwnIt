from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.config import settings
from app.core.logger import log
from app.schemas.health import HealthCheckResponse

router = APIRouter()


@router.get("/", response_model=HealthCheckResponse)
def check_health(db: Session = Depends(get_db)) -> HealthCheckResponse:
    """
    Check the application health and database connection status.
    Returns 'ok' if the database is reachable and the application is running.
    """
    log.info("Health check requested")
    db_status = "ok"

    try:
        db.execute(text("SELECT 1"))
        log.debug("Database connectivity verified successfully")
    except Exception as e:
        db_status = f"error: {str(e)}"
        log.exception("Health check failed due to database connectivity issue")

    return HealthCheckResponse(
        status="ok" if db_status == "ok" else "degraded",
        database=db_status,
        environment=settings.ENVIRONMENT.value,
        version=settings.VERSION,
    )
