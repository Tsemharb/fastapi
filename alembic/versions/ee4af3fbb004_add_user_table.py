"""add user table


Revision ID: ee4af3fbb004
Revises: f8b58e0510aa
Create Date: 2022-04-21 03:36:28.501339

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ee4af3fbb004'
down_revision = 'f8b58e0510aa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))


def downgrade():
    op.drop_table('users')
