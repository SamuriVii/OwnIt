from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

async_engine = create_async_engine(settings.ASYNC_DB_URL, echo=settings.DB_ECHO_SQL)

# expire_on_commit=False — prevents lazy loading errors after commit in async context
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
