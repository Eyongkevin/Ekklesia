import uuid

from sqlalchemy import ForeignKey, String, DateTime, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class ChurchTheme(Base):
    __tablename__ = "church_theme"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    church_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("churches.id"),
        nullable=False
    )

    year: Mapped[int] = mapped_column(nullable=False)
    theme: Mapped[str] = mapped_column(String, nullable=False)
    verse: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint("church_id", "year", name="unique_church_year"),
    )

    # relationship
    church: Mapped["Church"] = relationship(back_populates="themes")