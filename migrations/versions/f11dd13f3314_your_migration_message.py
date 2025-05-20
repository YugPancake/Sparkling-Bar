"""Add is_verified column to users table

Revision ID: f11dd13f3314
Revises: 56851a9173bc
Create Date: 2025-05-20 20:59:33.536372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f11dd13f3314'
down_revision: Union[str, None] = '56851a9173bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='0'))


def downgrade() -> None:

    op.drop_column('users', 'is_verified')
