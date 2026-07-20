from typing import Optional

from sqlalchemy.orm import Session
from app.models import SystemRole
from app.models import Permission


class SytemRoleCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        name: str,
        version: int = 1,
        description: Optional[str] = None, 
        is_active: bool = True,
        permissions: Optional[list[Permission]] = None
    ) -> SystemRole:
        system_role = SystemRole(
            name=name,
            version=version,
            description=description,
            is_active=is_active,
            permissions=permissions
        )
        self.db.add(system_role)

        return system_role
    
    def get_roles(self, is_active:bool) -> list[SystemRole]:
        return self.db.query(SystemRole).filter(SystemRole.is_active==is_active).all()

