from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api import deps
from app.services.user import UserService
from app.services.membership import MembershipService
from app.core.utils import MembershipRole
from app.schemas import user as user_schemas
from app.schemas import user_base as user_base_schemas
from app.core.security import create_access_token
from app.core.config import settings
from app.db.uow import UnitOfWork
from app.models import User


router = APIRouter(prefix="/users", tags=["Users_memberships"])



@router.post("/register", response_model=user_schemas.User)
def register_user(payload: user_schemas.InviteUserCreate, uow: UnitOfWork = Depends(deps.get_db)):
    return UserService(uow).register_user_with_invite(
        telegram_id=payload.telegram_id,
        first_name=payload.first_name,
        code=payload.invite_code
    )


@router.post("/login/", response_model=user_schemas.LoginResponse)
async def login_user(response: Response, payload:OAuth2PasswordRequestForm = Depends(),  uow: UnitOfWork = Depends(deps.get_db)):
    user=UserService(uow).authenticate_user(
        email=payload.username,
        password=payload.password
    )

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token: str = create_access_token(str(user.id))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=settings.SECURE
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get('/admin/', response_model=user_base_schemas.UserAdminListRes)
def get_admin_users_by_church(
    user: User = Depends(deps.get_user),
    filters: user_schemas.UserAdminFilterOptions = Depends(),
    uow: UnitOfWork = Depends(deps.get_db)
    ):
    return UserService(uow).get_admin_users_by_church(user.memberships[0].church_id, filters)

@router.get('/memberships/{church_id}/stats')
def membership_stats(church_id: str, uow: UnitOfWork = Depends(deps.get_db)) -> dict[str, dict[str, int]]:
    return MembershipService(uow).get_church_membership_stats(church_id)
