import uuid

from sqlalchemy import String, DateTime, UniqueConstraint, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Membership(Base):
    __tablename__ = "memberships"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    church_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("churches.id"),
        nullable=True # For super_user doesn't belong to any church
    )

    role: Mapped[str] = mapped_column(
        String,
        default="member" # super_admin, church_admin, member, prayer_team, 
    )

    is_active: Mapped[bool] = mapped_column(
        default=True
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

    user = relationship("User", back_populates="memberships")
    church = relationship("Church", back_populates="memberships")

    __table_args__ = (
        UniqueConstraint("user_id", "church_id", name="uq_user_church"),
    )

    def __repr__(self) -> str:
        return f'<Membership role={self.role}, is_active={self.is_active}>'