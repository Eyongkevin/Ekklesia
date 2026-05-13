from fastapi import APIRouter, Depends, Request

from app.api import deps
from app.services.invite import InviteService
from app.core.config import settings
from app.core.schemas.invite import InviteCreate
from app.db.uow import UnitOfWork

router = APIRouter(prefix="/invites", tags=["Invites"])


@router.post("/")
def create_invite(invite: InviteCreate, user = Depends(deps.get_user), uow: UnitOfWork = Depends(deps.get_db)):
    invite = InviteService(uow).create_invite(
        church_id=user.memberships[0].church_id,
        invite=invite
    )

    return {
        "code": invite.code,
        "link": f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={invite.code}"
    }