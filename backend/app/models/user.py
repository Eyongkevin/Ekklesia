import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, func, CheckConstraint, text, Index, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.core.utils import UserCreationSource


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    email: Mapped[str | None] = mapped_column(
        String(254),
        nullable=True,
    )

    telegram_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )

    first_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        default=True, server_default=text("true")
    )

    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    creation_source: Mapped[UserCreationSource] = mapped_column(
        Enum(
            UserCreationSource,
            name="user_creation_source",
            #! store web_app, sqladmin, bootstrap rather than WEB_APP, SQLADMIN, BOOTSTRAP
            values_callable=lambda enum_cls: [
                item.value for item in enum_cls
            ],
        ),
        nullable=False,
        default=UserCreationSource.WEB_APP,
        server_default=UserCreationSource.WEB_APP.value
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

    # cascade="all, delete-orphan"
    memberships = relationship("Membership", back_populates="user", passive_deletes="all")
    created_by: Mapped["User | None"] = relationship(
        "User",
        remote_side=[id],
        foreign_keys=[created_by_id]
    )

    __table_args__ = (
        Index(
            "uq_users_email_ci",
            func.lower(func.btrim(email)),
            unique=True,
        ),
        # TODO: If 'email' is not null, then 'password' should not be null.
        CheckConstraint(
            """
            NULLIF(btrim(email), '') IS NOT NULL
            OR
            NULLIF(btrim(telegram_id), '') IS NOT NULL
            """,
            name="ck_users_login_identifier",
        )

    )

    def __repr__(self) -> str:
        return f'{self.first_name} ({self.email})'