"""created users and documents tables

Revision ID: bc2f87c5bee3
Revises: 
Create Date: 2025-05-19 22:18:41.177603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bc2f87c5bee3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.TEXT(), nullable=False),
    sa.Column('email', sa.TEXT(), nullable=False),
    sa.Column('password', sa.TEXT(), nullable=False),
    sa.Column('plan', sa.TEXT(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('documents',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('pdf_url', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('pdf_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('documents')
    op.drop_table('users')
    # ### end Alembic commands ###
