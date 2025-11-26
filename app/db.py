from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config

# SQLAlchemy engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to use in FastAPI routes
def get_db():
    """
    Provide a SQLAlchemy session for FastAPI dependency injection.
    Usage:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
