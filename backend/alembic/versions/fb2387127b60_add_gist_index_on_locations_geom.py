"""add gist index on locations geom

Revision ID: fb2387127b60
Revises: 1facdab47d0e
Create Date: 2026-09-26 01:17:44.354057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = 'fb2387127b60'
down_revision: Union[str, Sequence[str], None] = '1facdab47d0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        'idx_locations_geom',
        'locations',
        ['geom'],
        unique=False,
        postgresql_using='gist',
    )


def downgrade() -> None:
    op.drop_index('idx_locations_geom', table_name='locations')