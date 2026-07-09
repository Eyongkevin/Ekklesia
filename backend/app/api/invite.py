from fastapi import APIRouter, Depends, status as http_status

from app.api import deps
from app.services import invite as invite_services
from app.schemas import invite as invite_schemas
from app.db.uow import UnitOfWork
from app.models import User


router = APIRouter(prefix="/invites", tags=["Invites"])



@router.post("/", response_model=invite_schemas.Invite, status_code=http_status.HTTP_201_CREATED)
def create_invite(invite: invite_schemas.InviteCreate, user: User = Depends(deps.get_user), uow: UnitOfWork = Depends(deps.get_db)):
    new_invite = invite_services.InviteService(uow).create_invite(
        church_id=user.memberships[0].church_id,
        user_id = str(user.id),
        invite=invite
    )
    return new_invite

@router.patch("/{invite_id}/", response_model=invite_schemas.Invite, status_code=http_status.HTTP_200_OK)
def update_invite(invite_id: str, invite: invite_schemas.InviteUpdate,  _: User = Depends(deps.get_user), uow: UnitOfWork = Depends(deps.get_db)):
    return invite_services.InviteService(uow).update(invite_id, invite)

@router.delete("/{invite_id}/", status_code=http_status.HTTP_204_NO_CONTENT)
def delete_invite(invite_id: str, _: User = Depends(deps.get_user), uow: UnitOfWork = Depends(deps.get_db)):
    invite_services.InviteService(uow).delete(invite_id)

@router.get("/", response_model=invite_schemas.InvitetListRes, status_code=http_status.HTTP_200_OK)
def get_invites(
    filters: invite_schemas.InviteFilterOptions = Depends(),
    user: User = Depends(deps.get_user),
    uow: UnitOfWork = Depends(deps.get_db)
    ):
    return invite_services.InviteService(uow).get_invites(
        church_id=user.memberships[0].church_id,
        filters=filters
    )