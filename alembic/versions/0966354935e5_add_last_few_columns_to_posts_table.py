"""add last few columns to posts table

Revision ID: 0966354935e5
Revises: a80719ca9dde
Create Date: 2022-04-21 03:50:11.815841

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0966354935e5'
down_revision = 'a80719ca9dde'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
