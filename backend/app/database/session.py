from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Creating database Engine & Session
engine = create_engine(str(settings.DB_URL), echo=settings.DB_ECHO_SQL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
