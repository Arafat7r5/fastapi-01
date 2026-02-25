"""adding foreign key to posts table

Revision ID: 99a8565c390c
Revises: 2f4851bb5435
Create Date: 2026-02-25 16:21:01.026099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99a8565c390c'
down_revision: Union[str, Sequence[str], None] = '2f4851bb5435'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1️⃣ Add column
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer(), nullable=False)
    )

    # 2️⃣ Create foreign key constraint
    op.create_foreign_key(
        "posts_owner_id_fkey",  # constraint name
        "posts",                # source table
        "users",                # referent table
        ["owner_id"],           # local column
        ["id"],                 # remote column
        ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "posts_owner_id_fkey",
        "posts",
        type_="foreignkey"
    )

    op.drop_column("posts", "owner_id")
    pass
