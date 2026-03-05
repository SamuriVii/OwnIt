from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal


# Defining database dependency function
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
