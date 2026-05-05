from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


announcement_tag_link = Table(
    "announcement_tag_link",
    Base.metadata,
    Column("announcement_id", UUID(as_uuid=True), ForeignKey("announcements.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("announcement_tags.id", ondelete="CASCADE"), primary_key=True),
)


announcement_audience_link = Table(
    "announcement_audience_link",
    Base.metadata,
    Column("announcement_id", UUID(as_uuid=True), ForeignKey("announcements.id", ondelete="CASCADE"), primary_key=True),
    Column("audience_id", UUID(as_uuid=True), ForeignKey("announcement_audience.id", ondelete="CASCADE"), primary_key=True),
)