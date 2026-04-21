from collections.abc import Iterator

from redis import Redis
from sqlalchemy.orm import Session

from app.database.redis import get_redis_client
from app.database.session import SessionLocal


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis() -> Iterator[Redis]:
    client = get_redis_client()
    try:
        yield client
    finally:
        client.close()
