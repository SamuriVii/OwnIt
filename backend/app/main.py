from fastapi import FastAPI
from pydantic import BaseModel

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs" if settings.is_dev else None,
    redoc_url="/redoc" if settings.is_dev else None,
)


class MessageResponse(BaseModel):
    message: str


class HealthCheckResponse(BaseModel):
    status: str
    project_name: str
    version: str
    environment: str
    is_dev: bool


@app.get("/", response_model=MessageResponse)
async def root() -> MessageResponse:
    return MessageResponse(message="Hello World")


@app.get("/healthcheck", response_model=HealthCheckResponse)
def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(
        status="ok",
        project_name=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT.value,
        is_dev=settings.is_dev,
    )
