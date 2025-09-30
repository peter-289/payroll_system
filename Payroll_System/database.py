from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# Engine creation
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite only
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Dependency for FastAPI routes (if you’ll add API later)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
