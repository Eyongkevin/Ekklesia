from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.membership import Membership
from app.schemas import membership as membership_schemas
from app.core.utils import MembershipRole

class MembershipCRUD:
    def __init__(self, db: Session):
        self.db = db

    def check_membership(self, user_id: str, church_id: str) -> membership_schemas.Membership | None:
        membership = self.db.query(Membership).filter_by(user_id=user_id, church_id=church_id).first()
        if membership:
            return membership_schemas.Membership.model_validate(membership)
        return None

    def create_membership(self, user_id: str, role: MembershipRole, church_id: str | None = None) -> membership_schemas.Membership:
        new_membership = Membership(
            user_id=user_id,
            role=role,
            church_id=church_id
        )
        self.db.add(new_membership)
        self.db.flush()
        return membership_schemas.Membership.model_validate(new_membership)
    
    def is_super_admin(self, user_id: str) -> bool:
        return self.db.query(Membership).filter_by(
            user_id=user_id,
            role=MembershipRole.SUPER_ADMIN,
            is_active=True
        ).first() is not None
    
    def is_church_admin(self, user_id: str) -> bool:
        return self.db.query(Membership).filter_by(
            user_id=user_id,
            role=MembershipRole.CHURCH_ADMIN,
            is_active=True
        ).first() is not None
    
    def get_user_church_membership(self, user_id: str) -> Optional[Membership]:
        return self.db.query(Membership).filter_by(
            user_id=user_id,
            is_active=True
        ).first()
    
    def get_church_membership_role_count(self, church_id: str):
        return (
            self.db.query(Membership.role, func.count(Membership.id))
            .filter_by(church_id=church_id)
            .group_by(Membership.role)
            .all()
        )
    
    def get_church_membership_category_count(self, church_id: str):
        return (
            self.db.query(Membership.category, func.count(Membership.id))
            .filter_by(church_id=church_id)
            .group_by(Membership.category)
            .all()
        )
