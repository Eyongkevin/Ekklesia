from fastapi import APIRouter, Depends

from app.api import deps
from app.services import invite as invite_services
from app.core.config import settings
from app.schemas import invite as invite_schemas
from app.db.uow import UnitOfWork
from app.models import User


router = APIRouter(prefix="/invites", tags=["Invites"])



@router.post("/", response_model=invite_schemas.InviteRes)
def create_invite(invite: invite_schemas.InviteCreate, user: User = Depends(deps.get_user), uow: UnitOfWork = Depends(deps.get_db)):
    invite_code = invite_services.InviteService(uow).create_invite(
        church_id=user.memberships[0].church_id,
        invite=invite
    )

    return {
        "code": invite_code.code,
        "link": f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={invite_code.code}"
    }
