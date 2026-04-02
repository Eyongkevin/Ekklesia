from sqlalchemy.orm import Session

from app.models.membership import Membership
from app.core.schemas import membership as membership_schemas

def check_membership(db: Session, user_id: str, church_id: str) -> membership_schemas.Membership | None:
    membership =  db.query(Membership).filter_by(user_id=user_id, church_id=church_id).first() 
    if membership:
        return membership_schemas.Membership.model_validate(membership)
    return None


def create_membership(db: Session, user_id: str, church_id: str) -> membership_schemas.Membership:
    new_membership = Membership(
        user_id=user_id,
        church_id=church_id
    )
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return membership_schemas.Membership.model_validate(new_membership)
