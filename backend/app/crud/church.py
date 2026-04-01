from sqlalchemy.orm import Session
from app.models.church import Church


def create_church(db: Session, name: str):
    print(f"Creating church: {name}")
    church = Church(
        name=name
    )
    db.add(church)
    db.commit()
    db.refresh(church)
    return church

def get_church_by_id(db: Session, church_id: str):
    return db.query(Church).filter(Church.id == church_id).first()

def get_churches(db: Session):
    return db.query(Church).all()
