from typing import Optional

from sqlalchemy.orm import Session
from app.models.permission import Permission


class PermissionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        code: str,
        name: str,
        description: Optional[str] = None, 
        is_active: bool = True
    ) -> Permission:
        permission = Permission(
            code=code,
            name=name,
            description=description,
            is_active=is_active
        )
        self.db.add(permission)

        return permission
    
    def get_permissions(self, is_active:bool) -> list[Permission]:
        return self.db.query(Permission).filter(Permission.is_active==is_active).all()
    
    def get_by_code(self, code: str) -> Optional[Permission]:
        return self.db.query(Permission).filter(Permission.code==code).scalar()

