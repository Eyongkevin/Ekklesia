from typing import Optional
import uuid

from app.repositories.role import RoleCRUD
from app.db.uow import UnitOfWork
from app.models import SystemRole, Permission, Role
from app.schemas import role as role_schemas
from app.services import permission as permission_services

class RoleService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.role_crud = RoleCRUD(self.uow.db)

    def create_bulk_from_system(self, church_id: str, roles: list[SystemRole]) -> list[Role]:
        created_roles: list[Role] = []

        for role in roles:
            new_role = self.role_crud.create(
                church_id=church_id,
                name=role.name,
                template_version=role.version,
                system_role_id=str(role.id),
                is_active=role.is_active,
                description=role.description,
                permissions=list(role.permissions)
            )
            created_roles.append(new_role)
        
        self.uow.commit()

        return created_roles


    def create(self, role: role_schemas.RoleReq):
        permissions: list[Permission] = permission_services.PermissionService(self.uow).get_by_codes(role.permissions)

        new_role = self.role_crud.create(
            church_id=str(role.church_id),
            name=role.name,
            template_version=role.template_version,
            system_role_id=str(role.system_role_id) if role.system_role_id else None,
            is_active=role.is_active,
            description=role.description,
            permissions=permissions
        )
        self.uow.commit()
        return new_role


    def get_system_roles(self, is_active:bool = True) -> list[SystemRole]:
        return self.role_crud.get_roles(is_active)