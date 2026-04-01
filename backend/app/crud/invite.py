from sqlalchemy.orm import Session
from app.models.invite_code import InviteCode

def get_active_invite_by_code(db: Session, code: str) -> InviteCode | None:
    return db.query(InviteCode).filter(
        InviteCode.code == code,
        InviteCode.is_active == True
    ).first()

def create_invite_code(db: Session, code: str, church_id: str):
    invite = InviteCode(
        code=code,
        church_id=church_id
    )

    db.add(invite)
    db.commit()
    db.refresh(invite)

    return invite