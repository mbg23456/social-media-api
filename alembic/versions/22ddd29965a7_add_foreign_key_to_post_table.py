"""add foreign key to post table

Revision ID: 22ddd29965a7
Revises: 969a019e4c2c
Create Date: 2025-08-05 21:41:34.399404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22ddd29965a7'
down_revision: Union[str, Sequence[str], None] = '969a019e4c2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'fk_posts_users',
        source_table = 'posts',
        referent_table = 'users',
        local_cols = ['owner_id'],
        remote_cols = ['id'],
        ondelete='CASCADE'
    )
    op.create_index('ix_posts_owner_id', 'posts', ['owner_id'])
    op.execute('UPDATE posts SET owner_id = 1')  # Set a default owner_id for existing posts
    op.alter_column('posts', 'owner_id', nullable=False)
    pass


def downgrade() -> None:
    op.drop_constraint('fk_posts_users', table_name = 'posts')
    op.drop_column('posts', 'owner_id')
    pass
