from sqlalchemy.orm import Session
from app.models.church import Church


class ChurchCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_church(self, name: str):
        print(f"Creating church: {name}")
        church = Church(
            name=name
        )
        self.db.add(church)
        self.db.commit()
        self.db.refresh(church)
        return church

    def get_church_by_id(self, church_id: str):
        return self.db.query(Church).filter(Church.id == church_id).first()

    def get_churches(self):
        return self.db.query(Church).all()
