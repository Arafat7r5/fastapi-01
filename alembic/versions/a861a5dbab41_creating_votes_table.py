"""creating votes table

Revision ID: a861a5dbab41
Revises: 99a8565c390c
Create Date: 2026-02-25 16:38:49.780997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a861a5dbab41'
down_revision: Union[str, Sequence[str], None] = '99a8565c390c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("user_id", "post_id")
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("votes")
    pass
