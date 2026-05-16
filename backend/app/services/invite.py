import random
import string
from app.repositories.invite import InviteCRUD
from app.services.church import ChurchService
from app.db.uow import UnitOfWork
from app.schemas import invite as schema_invite
from app.models import InviteCode

class InviteService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.invite_crud = InviteCRUD(self.uow.db)

    @staticmethod
    def generate_code(church_code: str, length: int = 6) -> str:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        return f"{church_code}-{code}"

    def create_invite(self, invite: schema_invite.InviteCreate, church_id: str) -> InviteCode:
        church_code = ChurchService(self.uow).get_church_code(church_id)
        code: str = InviteService.generate_code(church_code)
        invite_code = self.invite_crud.create_invite_code(code, church_id, invite.expires_at)
        self.uow.commit()
        return invite_code
    
    def validate_invite_code(self, code: str) -> InviteCode | None:
        return self.invite_crud.get_active_invite_by_code(code)

