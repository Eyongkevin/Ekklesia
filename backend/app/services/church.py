from app.crud.church import ChurchCRUD
from app.db.uow import UnitOfWork
from app.core.schemas.church import Church



class ChurchService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.church_crud = ChurchCRUD(self.uow.db)

    def create_church(self, name: str) -> Church:
        # return dict(id=1, name='Test Church')
        return self.church_crud.create_church(name)
    
    def get_church_by_id(self, church_id: str) -> Church:
        return self.church_crud.get_church_by_id(church_id)

    def get_churches(self) -> list[Church]:
        return self.church_crud.get_churches()