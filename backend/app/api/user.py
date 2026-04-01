from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.user import UserService
from app.core.schemas import user as user_schemas

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=user_schemas.User)
def register_user(payload: user_schemas.InviteUserCreate, db: Session = Depends(get_db)):
    return UserService.register_user_with_invite(
        db,
        telegram_id=payload.telegram_id,
        first_name=payload.first_name,
        code=payload.invite_code
    )
