from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.services.user import UserService
from app.core.schemas import user as user_schemas
from app.db.uow import UnitOfWork

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=user_schemas.User)
def register_user(payload: user_schemas.InviteUserCreate, uow: UnitOfWork = Depends(get_db)):
    return UserService(uow).register_user_with_invite(
        telegram_id=payload.telegram_id,
        first_name=payload.first_name,
        code=payload.invite_code
    )
