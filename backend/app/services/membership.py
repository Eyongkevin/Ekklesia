from sqlalchemy.orm import Session
from app.crud import membership
from app.core.schemas import membership as membership_schemas


def check_membership(db: Session, user_id: str, church_id: str) -> bool:
    return membership.check_membership(db, user_id, church_id) is not None

def create_membership(db: Session, user_id: str, church_id: str) -> membership_schemas.Membership:
    return membership.create_membership(db, user_id, church_id)