from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.services.invite import InviteService
from app.core.config import settings
from app.core.schemas.invite import InviteCreate
from app.db.uow import UnitOfWork

router = APIRouter(prefix="/invites", tags=["Invites"])


@router.post("/")
def create_invite(payload: InviteCreate, uow: UnitOfWork = Depends(get_db)):
    invite = InviteService(uow).create_invite(
        church_id=payload.church_id
    )

    return {
        "code": invite.code,
        "link": f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={invite.code}"
    }