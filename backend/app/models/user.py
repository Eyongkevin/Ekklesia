# import uuid
# from datetime import datetime

# from sqlalchemy import String, DateTime, func
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import Mapped, mapped_column

# from app.db.base import Base


# class User(Base):
#     __tablename__ = "users"

#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4
#     )

#     telegram_id: Mapped[str] = mapped_column(
#         String,
#         unique=True,
#         nullable=False,
#         index=True
#     )

#     first_name: Mapped[str] = mapped_column(
#         String,
#         nullable=True
#     )

#     role: Mapped[str] = mapped_column(
#         String,
#         default="guest" # member, prayer_team, admin
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         server_default=func.now()
#     )

#     modified_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         server_default=func.now(),
#         onupdate=func.now()
#     )

#     def __repr__(self) -> str:
#         return f'<User {self.telegram_id}>'