from typing import Optional
import uuid

from app.repositories.role import RoleCRUD
from app.db.uow import UnitOfWork
from app.models import SystemRole, Permission, Role
from app.schemas import role as role_schemas
from app.services import permission as permission_services
from app.core.exceptions import role as role_exceptions

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


    def create(self, church_id: str, role: role_schemas.RoleReq):
        permissions: list[Permission] = permission_services.PermissionService(self.uow).get_by_names(role.permissions)

        new_role = self.role_crud.create(
            church_id=church_id,
            name=role.name,
            template_version=role.template_version,
            system_role_id=str(role.system_role_id) if role.system_role_id else None,
            is_active=role.is_active,
            description=role.description,
            permissions=permissions
        )
        self.uow.commit()
        return new_role


    def get_roles(self, church_id: str, filters: role_schemas.RoleFilterOptions, is_active:bool = True) -> list[Role]:
        offset = (filters.page - 1) * filters.per_page
        return self.role_crud.get_roles(church_id, is_active, search=filters.search, offset=offset, limit=filters.per_page)

    def update(self, role_id: str, role: role_schemas.RoleReq)-> Role:
        existing_role: Role | None = self.role_crud.get_by_id(role_id)

        if not existing_role:
            raise role_exceptions.RoleNotFound

        existing_role.name = role.name
        existing_role.description = role.description
        existing_role.is_customized = True
        
        existing_role.permissions = permission_services.PermissionService(self.uow).get_by_names(role.permissions)

        self.uow.commit()

        return existing_role
        


