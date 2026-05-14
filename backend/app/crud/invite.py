from typing import Optional
from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.invite_code import InviteCode


class InviteCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_active_invite_by_code(self, code: str) -> InviteCode | None:
        return self.db.query(InviteCode).filter(
            InviteCode.code == code,
            InviteCode.is_active == True,
            or_(
                InviteCode.expires_at.is_(None),
                InviteCode.expires_at > datetime.now()
            )
    ).first()

    def create_invite_code(self, code: str, church_id: str, expires_at: Optional[datetime] = None):
        invite = InviteCode(
            code=code,
            church_id=church_id,
            expires_at=expires_at
        )

        self.db.add(invite)
        self.db.commit()
        self.db.refresh(invite)

        return invite
