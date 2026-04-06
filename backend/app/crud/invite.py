from sqlalchemy.orm import Session
from app.models.invite_code import InviteCode


class InviteCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_active_invite_by_code(self, code: str) -> InviteCode | None:
        return self.db.query(InviteCode).filter(
            InviteCode.code == code,
            InviteCode.is_active == True
    ).first()

    def create_invite_code(self, code: str, church_id: str):
        invite = InviteCode(
            code=code,
            church_id=church_id
        )

        self.db.add(invite)
        self.db.commit()
        self.db.refresh(invite)

        return invite
