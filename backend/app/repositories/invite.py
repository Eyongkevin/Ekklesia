from typing import Optional
from datetime import datetime

from sqlalchemy import or_, func
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

    def create_invite_code(self, code: str, church_id: str, user_id: str, state: bool, expires_at: Optional[datetime] = None) -> InviteCode:
        invite = InviteCode(
            code=code,
            church_id=church_id,
            user_id=user_id,
            is_active=state,
            expires_at=expires_at
        )

        self.db.add(invite)

        return invite
    
    def get_invite_by_id(self, id: str) -> InviteCode | None:
        return self.db.query(InviteCode).get(id)

    def get_invites(
        self,
        church_id: str,
        state: Optional[str],
        is_active: Optional[bool],
        offset: int = 0,
        limit: int = 10
    ) -> tuple[list[InviteCode], int]:
        query = self.db.query(InviteCode).filter(InviteCode.church_id == church_id)
        if is_active is not None:
            query = query.filter(InviteCode.is_active.is_(is_active))
        if state is not None:
            if state == "VALID":
                query = query.filter(or_(InviteCode.expires_at > func.now(), InviteCode.expires_at.is_(None)))
            elif state == "EXPIRED":
                query = query.filter(InviteCode.expires_at < func.now())
            elif state == "NEVER":
                query = query.filter(InviteCode.expires_at.is_(None))

        total = query.count()

        invites = query.order_by(InviteCode.created_at.desc()).offset(offset).limit(limit).all()

        return invites, total

    def delete(self, invite: InviteCode) -> None:
        self.db.delete(invite)
