from typing import Optional
import uuid

from app.repositories.role import SytemRoleCRUD
from app.db.uow import UnitOfWork
from app.models import SystemRole, Permission
from app.schemas import role as role_schemas
from app.services import permission as permission_services

class SystemRoleService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.role_crud = SytemRoleCRUD(self.uow.db)

    def create(self, role: role_schemas.SystemRoleReq):
        permissions: list[Permission] = permission_services.PermissionService(self.uow).get_by_codes(role.permissions)

        new_role = self.role_crud.create(
            name=role.name,
            version=role.version,
            is_active=role.is_active,
            description=role.description,
            permissions=permissions
        )
        self.uow.commit()
        return new_role


    def get_system_roles(self, is_active:bool = True) -> list[SystemRole]:
        return self.role_crud.get_roles(is_active)