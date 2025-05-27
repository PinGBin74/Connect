"""fix

Revision ID: 7737101cd21a
Revises: 80eed0eb0a05
Create Date: 2025-05-27 23:55:06.403369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7737101cd21a'
down_revision: Union[str, None] = '80eed0eb0a05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
