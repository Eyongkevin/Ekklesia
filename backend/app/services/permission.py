from typing import Optional
import uuid

from app.repositories.permission import PermissionCRUD
from app.db.uow import UnitOfWork
from app.models import Permission
from app.schemas import permission as permission_schemas

class PermissionService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.permission_crud = PermissionCRUD(self.uow.db)

    def create(self, permission: permission_schemas.PermissionReq):
        new_permission = self.permission_crud.create(
            name=permission.name,
            code=permission.code,
            is_active=permission.is_active,
            description=permission.description
        )
        self.uow.commit()
        return new_permission


    def get_permissions(self, is_active:bool = True) -> list[Permission]:
        return self.permission_crud.get_permissions(is_active)
    
    def get_by_code(self, code: str) -> Optional[Permission]:
        return self.permission_crud.get_by_code(code)
    
    def get_by_codes(self, codes: list[str]) -> list[Permission]:
        permissions: list[Permission] = []
        for code in codes:
            permission = self.get_by_code(code)
            if permission:
                permissions.append(permission)
        return permissions
