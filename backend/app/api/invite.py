from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.invite import InviteService
from app.core.config import settings
from app.core.schemas.invite import InviteCreate

router = APIRouter(prefix="/invites", tags=["Invites"])


@router.post("/")
def create_invite(payload: InviteCreate, db: Session = Depends(get_db)):
    invite = InviteService.create_invite(
        db,
        church_id=payload.church_id
    )

    return {
        "code": invite.code,
        "link": f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={invite.code}"
    }