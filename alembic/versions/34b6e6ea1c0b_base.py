"""base

Revision ID: 34b6e6ea1c0b
Revises:
Create Date: 2025-05-28 10:41:49.655721

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "34b6e6ea1c0b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
