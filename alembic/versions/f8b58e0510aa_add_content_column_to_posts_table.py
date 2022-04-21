"""add content column to posts table

Revision ID: f8b58e0510aa
Revises: cc0a10696e3c
Create Date: 2022-04-21 03:32:32.581689

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f8b58e0510aa'
down_revision = 'cc0a10696e3c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
