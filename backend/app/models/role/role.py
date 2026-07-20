from typing import Optional

import uuid

from sqlalchemy import String, DateTime, Text, Boolean, Integer, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from ..associations import role_permissions, membership_roles


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    church_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("churches.id", ondelete="CASCADE"),
        nullable=False
    )

    system_role_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("system_roles.id", ondelete="SET NULL"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    template_version: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    is_customized: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    modified_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles",
    )

    memberships = relationship(
        "Membership",
        secondary=membership_roles,
        back_populates="roles",
    )
    

    church = relationship("Church", back_populates="roles")
    system_role= relationship("SystemRole")

    __table_args__ = (
        UniqueConstraint("church_id", "name", name="uq_church_name"),
    )

    def __repr__(self) -> str:
        return f'{self.name}'
