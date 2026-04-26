from fastapi import APIRouter, Response
from sqlalchemy import text

from app.api.dependencies import AsyncDB, AsyncRedisClient
from app.core.config import settings
from app.core.logger import log
from app.schemas.health import (
    DatabaseHealthResponse,
    LivenessResponse,
    OverallHealthResponse,
    RedisHealthResponse,
)

router = APIRouter()


@router.get("/live", response_model=LivenessResponse)
async def check_liveness() -> LivenessResponse:
    return LivenessResponse(
        status="ok",
        environment=settings.ENVIRONMENT.value,
        version=settings.VERSION,
    )


@router.get("/db", response_model=DatabaseHealthResponse)
async def check_db_health(
    response: Response,
    db: AsyncDB,
) -> DatabaseHealthResponse:
    log.info("Database health check requested")
    db_status = "ok"

    try:
        await db.execute(text("SELECT 1"))
        log.debug("Database connectivity verified")
    except Exception as e:
        db_status = f"error: {e}"
        log.exception("Database health check failed")
        response.status_code = 503

    return DatabaseHealthResponse(
        status="ok" if db_status == "ok" else "degraded",
        database=db_status,
        environment=settings.ENVIRONMENT.value,
        version=settings.VERSION,
    )


@router.get("/redis", response_model=RedisHealthResponse)
async def check_redis_health(
    response: Response,
    redis: AsyncRedisClient,
) -> RedisHealthResponse:
    log.info("Redis health check requested")
    redis_status = "ok"

    try:
        await redis.ping()  # type: ignore[misc]
        log.debug("Redis connectivity verified")
    except Exception as e:
        redis_status = f"error: {e}"
        log.exception("Redis health check failed")
        response.status_code = 503

    return RedisHealthResponse(
        status="ok" if redis_status == "ok" else "degraded",
        redis=redis_status,
        environment=settings.ENVIRONMENT.value,
        version=settings.VERSION,
    )


@router.get("/", response_model=OverallHealthResponse)
async def check_overall_health(
    response: Response,
    db: AsyncDB,
    redis: AsyncRedisClient,
) -> OverallHealthResponse:
    log.info("Overall health check requested")
    db_status = "ok"
    redis_status = "ok"

    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {e}"
        log.exception("Database unreachable during overall health check")

    try:
        await redis.ping()  # type: ignore[misc]
    except Exception as e:
        redis_status = f"error: {e}"
        log.exception("Redis unreachable during overall health check")

    all_ok = db_status == "ok" and redis_status == "ok"
    if not all_ok:
        response.status_code = 503

    return OverallHealthResponse(
        status="ok" if all_ok else "degraded",
        database=db_status,
        redis=redis_status,
        environment=settings.ENVIRONMENT.value,
        version=settings.VERSION,
    )
