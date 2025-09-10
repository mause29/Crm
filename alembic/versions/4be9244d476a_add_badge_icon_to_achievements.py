"""Add badge_icon to achievements

Revision ID: 4be9244d476a
Revises: d9439dc18973
Create Date: 2025-09-07 06:16:55.450083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4be9244d476a'
down_revision: Union[str, Sequence[str], None] = 'd9439dc18973'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('achievements', sa.Column('badge_icon', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('achievements', 'badge_icon')
