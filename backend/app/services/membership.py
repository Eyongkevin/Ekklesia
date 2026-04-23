from app.crud.membership import MembershipCRUD
from app.core.schemas import membership as membership_schemas
from app.db.uow import UnitOfWork
from app.core.utils import MembershipRole


class MembershipService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.membership_crud = MembershipCRUD(self.uow.db)

    def check_membership(self, user_id: str, church_id: str) -> bool:
        return self.membership_crud.check_membership(user_id, church_id) is not None

    def create_membership(self, user_id: str, role: MembershipRole, church_id: str | None = None) -> membership_schemas.Membership:
        return self.membership_crud.create_membership(user_id, role, church_id)

    def check_is_super_admin(self, user_id: str) -> bool:
        return self.membership_crud.is_super_admin(user_id)
    
    def check_is_church_admin(self, user_id: str) -> bool:
        return self.membership_crud.is_church_admin(user_id)
    
    def user_church_membership(self, user_id: str) -> membership_schemas.Membership | None:
        return self.membership_crud.get_user_church_membership(user_id)