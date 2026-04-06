import random
import string
from app.crud.invite import InviteCRUD
from app.db.uow import UnitOfWork

class InviteService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.invite_crud = InviteCRUD(self.uow.db)

    @staticmethod
    def generate_code(length: int = 6) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def create_invite(self, church_id: str):
        code: str = InviteService.generate_code()
        return self.invite_crud.create_invite_code(code, church_id)
    
    def validate_invite_code(self, code: str):
        return self.invite_crud.get_active_invite_by_code(code)

