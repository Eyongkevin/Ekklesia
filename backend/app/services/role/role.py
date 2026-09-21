from typing import Optional
import uuid

from app.repositories.role import RoleCRUD
from app.db.uow import UnitOfWork
from app.models import SystemRole, Permission, Role
from app.schemas import role as role_schemas
from app.services import permission as permission_services
from app.services import user as user_services
from app.core.exceptions import role as role_exceptions

class RoleService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.role_crud = RoleCRUD(self.uow.db)

    def __resolve_filter(self, item: str) -> bool | int | None:
        if item == "True":
            return True
        elif item == "False":
            return False
        try:
            return int(item)
        except ValueError:
            pass


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


    def get_all_roles(self, church_id: str, is_active: bool = True) -> list[Role]:
        return self.role_crud.get_all_roles(church_id, is_active)

    def get_unique_template_versions(self):
        all_versions: list[int] = []
        versions =  self.role_crud.get_unique_template_versions()

        for (version, )  in versions:
            if version is not None:
                all_versions.append(version)
        return all_versions

    def get_roles(self, church_id: str, filters: role_schemas.RoleFilterOptions, is_active:bool = True) -> list[Role]:
        offset = (filters.page - 1) * filters.per_page
        return self.role_crud.get_roles(
            church_id, 
            is_active, 
            search=filters.search,
            from_system=self.__resolve_filter(filters.from_system),
            version=self.__resolve_filter(filters.version),
            # active=filters.active,
            customized = self.__resolve_filter(filters.customized),
            offset=offset, 
            limit=filters.per_page)


    def update_state(self, role_id: str, state: role_schemas.RoleStatusUpdate) -> Role:
        role: Role | None = self.role_crud.get_by_id(role_id)

        if not role:
            raise role_exceptions.RoleNotFound

        role.is_active = state.is_active
        self.uow.commit()

        return role


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

    def get_role_by_id_with_memberships(self, role_id: str):
        return self.role_crud.get_by_id_with_memberships(role_id)

    def delete(self, role_id: str) -> None:
        role: Role = self.role_crud.get_by_id(role_id)
        if not role:
            raise role_exceptions.RoleNotFound("Role to be deleted not found")
        if role.is_protected:
            raise role_exceptions.RoleProtectedError("This role is required by the church and cannot be deleted.")
        self.role_crud.delete(role)
        self.uow.commit()

    def merge_role(self, source_role_id: str, target_role_name: role_schemas.RoleMerge):
        try:
            source = self.role_crud.get_by_id(source_role_id)
            target = self.role_crud.get_by_name(target_role_name.target_role_name)

            user_service = user_services.UserService(self.uow)

            users = user_service.get_users_by_role(source_role_id)

            for user in users:
                if not user_service.has_role(user.id, target.id):
                    user_service.assign_role(user.id, target)

            self.role_crud.delete(source)

            self.uow.commit()
            return users

        except Exception:
            self.uow.rollback()
            raise





