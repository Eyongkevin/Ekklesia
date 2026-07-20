from typing import Optional

from sqlalchemy.orm import Session
from app.models import Role
from app.models import Permission


class RoleCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        church_id: str,
        name: str,
        template_version: int = 1,
        system_role_id: Optional[str] = None,
        description: Optional[str] = None, 
        is_customized: bool = False,
        is_active: bool = True,
        permissions: Optional[list[Permission]] = None
    ) -> Role:
        role = Role(
            church_id=church_id,
            name=name,
            template_version=template_version,
            system_role_id=system_role_id,
            description=description,
            is_customized=is_customized,
            is_active=is_active,
            permissions=permissions
        )
        self.db.add(role)

        return role
    
    def get_roles(self, is_active:bool) -> list[Role]:
        return self.db.query(Role).filter(Role.is_active==is_active).all()

