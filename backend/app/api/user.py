from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.deps import get_db
from app.services.user import UserService
from app.services.membership import MembershipService
from app.core.utils import MembershipRole
from app.schemas import user as user_schemas
from app.core.security import create_access_token
from app.core.config import settings
from app.db.uow import UnitOfWork


router = APIRouter(prefix="/users", tags=["Users_memberships"])



@router.post("/register", response_model=user_schemas.User)
def register_user(payload: user_schemas.InviteUserCreate, uow: UnitOfWork = Depends(get_db)):
    return UserService(uow).register_user_with_invite(
        telegram_id=payload.telegram_id,
        first_name=payload.first_name,
        code=payload.invite_code
    )


@router.post("/login/", response_model=user_schemas.LoginResponse)
async def login_user(payload: user_schemas.LoginRequest, response: Response, uow: UnitOfWork = Depends(get_db)):
    user=UserService(uow).authenticate_user(
        email=payload.email,
        password=payload.password
    )

    if user is None or not MembershipService(uow).check_is_church_admin(str(user.id)):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token: str = create_access_token(str(user.id), MembershipRole.CHURCH_ADMIN)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.SECURE
    )

    return {
        "message": "Login successful",
        "user": user,
        "access_token": token
    }


@router.get('/memberships/{church_id}/stats')
def membership_stats(church_id: str, uow: UnitOfWork = Depends(get_db)) -> dict[str, dict[str, int]]:
    return MembershipService(uow).get_church_membership_stats(church_id)
