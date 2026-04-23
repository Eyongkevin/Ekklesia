from typing import Optional

import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, func, DateTime, ForeignKey

from app.db.base import Base


class ChurchContact(Base):
    __tablename__ = "church_contact"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    church_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("churches.id"),
        nullable=False,
        unique=True
    )

    country: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address_line: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    phone_1: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone_2: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    facebook: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    youtube: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    instagram: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    modified_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    church = relationship("Church", back_populates="contact")
