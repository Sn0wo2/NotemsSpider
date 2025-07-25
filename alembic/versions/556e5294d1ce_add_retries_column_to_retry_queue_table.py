"""Add retries column to retry_queue table

Revision ID: 556e5294d1ce
Revises:
Create Date: 2025-07-22 02:51:10.996354

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "556e5294d1ce"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("retry_queue", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("retries", sa.Integer(), nullable=False, server_default="0")
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("retry_queue", schema=None) as batch_op:
        batch_op.drop_column("retries")
    # ### end Alembic commands ###
