"""add phone number

Revision ID: 3f5859565047
Revises: 73977149da92
Create Date: 2025-08-05 21:53:35.751268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f5859565047'
down_revision: Union[str, Sequence[str], None] = '73977149da92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
    pass
