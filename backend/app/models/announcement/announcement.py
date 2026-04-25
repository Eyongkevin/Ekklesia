from typing import Optional
import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, String, Boolean, Text, DateTime, CheckConstraint
from sqlalchemy.sql import func

from app.db.base import Base
from .associations import announcement_audience_link, announcement_tag_link

class Announcement(Base):
    __tablename__ = "announcements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("announcement_status.id"),
        nullable=False
    )

    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    publish_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    expire_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # event_id: Mapped[Optional[uuid.UUID]] = mapped_column(
    #     UUID(as_uuid=True),
    #     ForeignKey("events.id", ondelete="SET NULL"),
    #     nullable=True
    # )

    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
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

    # Relationships
    status: Mapped["AnnouncementStatus"] = relationship(
        back_populates="announcements"
    )

    tags: Mapped[list["AnnouncementTag"]] = relationship(
        secondary=announcement_tag_link,
        back_populates="announcements"
    )

    audiences: Mapped[list["AnnouncementAudience"]] = relationship(
        secondary=announcement_audience_link,
        back_populates="announcements"
    )

    # -------------------------
    # Constraints
    # -------------------------
    __table_args__ = (

        # Expire must be after publish
        CheckConstraint(
            "(expire_at IS NULL OR publish_at IS NULL OR expire_at > publish_at)",
            name="check_expire_after_publish"
        ),
    )