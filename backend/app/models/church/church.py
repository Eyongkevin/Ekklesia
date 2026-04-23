import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, func, DateTime

from app.db.base import Base


class Church(Base):
    __tablename__ = "churches"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String,
        unique=True, 
        nullable=False)

    # TODO: Set limit to be 6 characters
    code: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    is_active: Mapped[bool] = mapped_column(
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    memberships = relationship("Membership", back_populates="church", cascade="all, delete-orphan")
    contact = relationship("ChurchContact", back_populates="church", uselist=False, cascade="all, delete-orphan")
    themes = relationship("ChurchTheme", back_populates="church", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return self.name