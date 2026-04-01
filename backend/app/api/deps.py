from sqlalchemy.orm import Session
from app.db.session import SessionLocal  # your SQLAlchemy session factory

def get_db():
    """
    FastAPI dependency that yields a SQLAlchemy session.
    Ensures the session is closed after use.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()