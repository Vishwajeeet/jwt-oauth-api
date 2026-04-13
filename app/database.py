from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import QueuePool, NullPool
from app.config import settings
import ssl

class Base(DeclarativeBase):
    """Base class for all ORM models (SQLAlchemy 2.0 style)."""
    pass

# Configure connection pooling based on environment
# For Supabase/Render: use minimal pooling for better connection management
if settings.ENVIRONMENT == "production":
    # Production: Use connection pooling with proper SSL
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Test connections before using
        pool_recycle=3600,   # Recycle connections after 1 hour
        echo=False
    )
else:
    # Development: Single-threaded null pool for simplicity
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
        echo=True if settings.ENVIRONMENT == "development" else False
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()