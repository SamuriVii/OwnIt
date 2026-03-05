from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str
    database: str
    environment: str
    version: str
