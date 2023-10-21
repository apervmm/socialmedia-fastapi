"""add content Column to posts table

Revision ID: f4a0534d495b
Revises: 9758e799077d
Create Date: 2023-10-20 18:07:43.724869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4a0534d495b'
down_revision: Union[str, None] = '9758e799077d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
