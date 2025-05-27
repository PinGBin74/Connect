"""

Revision ID: 80eed0eb0a05
Revises: 74ada424232e
Create Date: 2025-05-27 23:54:43.360421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80eed0eb0a05'
down_revision: Union[str, None] = '74ada424232e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
