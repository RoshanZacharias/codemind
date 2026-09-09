"""add embeddings to code chunks

Revision ID: 8b512d8f5b5e
Revises: 0dd8936aedde
Create Date: 2026-09-09 10:06:20.041724

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = "8b512d8f5b5e"
down_revision: Union[str, Sequence[str], None] = "0dd8936aedde"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "code_chunks",
        sa.Column(
            "embedding",
            Vector(1536),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("code_chunks", "embedding")