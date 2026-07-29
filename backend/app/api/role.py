from fastapi import APIRouter, Depends, status as http_status

from app.api import deps
from app.services import role as role_services
from app.schemas import role as role_schemas
from app.db.uow import UnitOfWork
from app.models import User


router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=role_schemas.RoleRes, status_code=http_status.HTTP_201_CREATED)
def create(role: role_schemas.RoleReq, user: User = Depends(deps.get_user), uow: UnitOfWork = Depends(deps.get_db)):
    new_role = role_services.RoleService(uow).create(
        church_id=user.memberships[0].church_id,
        role=role
    )
    return new_role

@router.get("/", response_model=role_schemas.RoleListRes, status_code=http_status.HTTP_200_OK)
def get_roles(
    user: User = Depends(deps.get_user),
    filters: role_schemas.RoleFilterOptions = Depends(),
    uow: UnitOfWork = Depends(deps.get_db)
    ):
    return role_services.RoleService(uow).get_roles(church_id=user.memberships[0].church_id, filters=filters)

@router.patch("/{role_id}/", response_model=role_schemas.RoleRes, status_code=http_status.HTTP_200_OK)
def update(
    role_id: str,
    role: role_schemas.RoleReq,
    _: User = Depends(deps.get_user),
    uow: UnitOfWork = Depends(deps.get_db)
    ):
    return role_services.RoleService(uow).update(role_id, role)