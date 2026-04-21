from pydantic import BaseModel


class BaseHealthResponse(BaseModel):
    status: str
    environment: str
    version: str


class LivenessResponse(BaseHealthResponse):
    pass


class DatabaseHealthResponse(BaseHealthResponse):
    database: str


class RedisHealthResponse(BaseHealthResponse):
    redis: str


class OverallHealthResponse(BaseHealthResponse):
    database: str
    redis: str
