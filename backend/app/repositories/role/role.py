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
        template_version: Optional[int] = None,
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
    
    def get_roles(self, church_id: str, is_active:bool, search: str, offset: int=0, limit: int=10) -> dict[str, int | list[Role]]:
        query = self.db.query(Role).filter(Role.church_id==church_id, Role.is_active==is_active)

        if search:
            query = query.filter(Role.name.ilike(f'%{search}%'))
        total = query.count()
        roles = (query
                .order_by(Role.created_at.desc())
                .offset(offset)
                .limit(limit)
                .all())
        return {
            'roles': roles,
            'total': total
        }

    def get_by_id(self, role_id: str) -> Role | None:
            role = self.db.query(Role).get(role_id)
            return role

