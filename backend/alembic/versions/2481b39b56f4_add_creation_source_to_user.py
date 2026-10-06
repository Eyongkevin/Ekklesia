"""add creation_source to User

Revision ID: 2481b39b56f4
Revises: 9b9d0058f4ba
Create Date: 2026-10-06 21:38:14.203917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '2481b39b56f4'
down_revision: Union[str, Sequence[str], None] = '9b9d0058f4ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_creation_source = postgresql.ENUM(
    'web_app', 'sqladmin', 'bootstrap',
    name='user_creation_source',
    create_type=False,
)


def upgrade() -> None:
    """Upgrade schema."""
    user_creation_source.create(op.get_bind(), checkfirst=True)
    op.add_column('users', sa.Column(
        'creation_source', user_creation_source,
        server_default='web_app', nullable=False,
    ))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'creation_source')
    user_creation_source.drop(op.get_bind(), checkfirst=True)
