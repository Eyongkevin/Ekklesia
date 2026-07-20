from fastapi import APIRouter, Depends, status as http_status

from app.api import deps
from app.services import role as role_services
from app.schemas import role as role_schemas
from app.db.uow import UnitOfWork
from app.models import User


router = APIRouter(prefix="/system-roles", tags=["System Roles"])



@router.post("/", response_model=role_schemas.SystemRoleRes, status_code=http_status.HTTP_201_CREATED)
def create_system_role(role: role_schemas.SystemRoleReq, _: User = Depends(deps.get_user), uow: UnitOfWork = Depends(deps.get_db)):
    new_role = role_services.SystemRoleService(uow).create(role)
    return new_role

# @router.get("/", response_model=invite_schemas.InvitetListRes, status_code=http_status.HTTP_200_OK)
# def get_invites(
#     filters: invite_schemas.InviteFilterOptions = Depends(),
#     user: User = Depends(deps.get_user),
#     uow: UnitOfWork = Depends(deps.get_db)
#     ):
#     return invite_services.InviteService(uow).get_invites(
#         church_id=user.memberships[0].church_id,
#         filters=filters
#     )