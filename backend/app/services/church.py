from sqlalchemy.orm import Session

from app.crud.church import create_church, get_church_by_id, get_churches
from app.core.schemas.church import Church, ChurchCreate



class ChurchService:
    @staticmethod
    def create_church(db: Session, name: str) -> Church:
        # return dict(id=1, name='Test Church')
        return create_church(db, name)
    
    @staticmethod
    def get_church_by_id(db: Session, church_id: str) -> Church:
        return get_church_by_id(db, church_id)
    
    @staticmethod
    def get_churches(db: Session) -> list[Church]:
        return get_churches(db)