from fastapi import APIRouter, Depends, status as http_status

from app.api import deps
from app.services import role as role_services
from app.schemas import role as role_schemas
from app.schemas import user as user_schemas
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

@router.get("/all/", response_model=list[role_schemas.RoleAllRes], status_code=http_status.HTTP_200_OK)
def get_all_roles(
    user: User = Depends(deps.get_user),
    uow: UnitOfWork = Depends(deps.get_db)
    ):
    return role_services.RoleService(uow).get_all_roles(church_id=user.memberships[0].church_id)

@router.get("/template_versions/")
def get_unique_template_versions(uow: UnitOfWork = Depends(deps.get_db)):
    return role_services.RoleService(uow).get_unique_template_versions()

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

@router.delete("/{role_id}/", status_code=http_status.HTTP_204_NO_CONTENT)
def delete(role_id: str,  _: User = Depends(deps.get_user), uow: UnitOfWork = Depends(deps.get_db)) -> None:
    return role_services.RoleService(uow).delete(role_id)

@router.get("/{role_id}/", response_model=role_schemas.RoleRes, status_code=http_status.HTTP_200_OK)
def roles_with_memberships(role_id: str,  _: User = Depends(deps.get_user), uow: UnitOfWork = Depends(deps.get_db)):
    return role_services.RoleService(uow).get_role_by_id_with_memberships(role_id)

@router.post("/{role_id}/merge/", response_model=list[user_schemas.User])
def merge_role(role_id: str, target_role_name: role_schemas.RoleMerge, _: User = Depends(deps.get_user), uow: UnitOfWork = Depends(deps.get_db)):
    return role_services.RoleService(uow).merge_role(role_id, target_role_name)