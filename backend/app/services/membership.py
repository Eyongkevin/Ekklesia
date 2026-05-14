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

    def create_membership(self, user_id: str, role: MembershipRole | None = None, church_id: str | None = None) -> membership_schemas.Membership:
        return self.membership_crud.create_membership(
            user_id, 
            role if role is not None else MembershipRole.MEMBER,
            church_id)

    def check_is_super_admin(self, user_id: str) -> bool:
        return self.membership_crud.is_super_admin(user_id)
    
    def check_is_church_admin(self, user_id: str) -> bool:
        return self.membership_crud.is_church_admin(user_id)
    
    def user_church_membership(self, user_id: str) -> membership_schemas.Membership | None:
        return self.membership_crud.get_user_church_membership(user_id)
    
    def get_church_membership_stats(self, church_id: str) -> dict[str, dict[str, int]]:
        role_counts = self.membership_crud.get_church_membership_role_count(church_id)
        category_counts = self.membership_crud.get_church_membership_category_count(church_id)

        return {
            'role_counts': {role: count for role, count in role_counts},
            'category_counts': {cat: count for cat, count in category_counts if cat}
        }
