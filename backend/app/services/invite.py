import random
import string
from app.repositories.invite import InviteCRUD
from app.services.church import ChurchService
from app.db.uow import UnitOfWork
from app.schemas import invite as schema_invite
from app.models import InviteCode
from app.core.exceptions import invite as invite_exceptions

class InviteService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.invite_crud = InviteCRUD(self.uow.db)

    def create_invite(self, invite: schema_invite.InviteCreate, church_id: str, user_id: str) -> InviteCode:
        church_code = ChurchService(self.uow).get_church_code(church_id)
        invite_code = self.invite_crud.create_invite_code(f"{church_code}-{invite.code}", church_id, user_id, invite.state, invite.expires_at)
        self.uow.commit()
        return invite_code
    
    def update(self, invite_id: str, data: schema_invite.InviteUpdate) -> InviteCode:
        invite = self.invite_crud.get_invite_by_id(invite_id)
        if invite is None:
            raise invite_exceptions.InviteNotFound()
        
        update_invite_data = data.model_dump(exclude_unset=True)
        for field, value in update_invite_data.items():
            setattr(invite, field, value)

        self.uow.commit()
        return invite
    
    def delete(self, invite_id: str):
        invite = self.invite_crud.get_invite_by_id(invite_id)
        if not invite:
            raise invite_exceptions.InviteNotFound()
        self.invite_crud.delete(invite)

        self.uow.commit()


    
    def validate_invite_code(self, code: str) -> InviteCode | None:
        return self.invite_crud.get_active_invite_by_code(code)
    
    def get_invites(self, church_id: str, filters: schema_invite.InviteFilterOptions) -> dict[str, list[InviteCode] | int]:
        offset = (filters.page - 1) * filters.per_page
        invites, total = self.invite_crud.get_invites(
            church_id = church_id,
            state = filters.state,
            is_active = filters.is_active,
            offset = offset,
            limit = filters.per_page
        )

        return {
            "invites": invites,
            "total": total
        }
