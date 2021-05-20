"""Create _no_device

Revision ID: b35a36b589f8
Revises: 9030aa258427
Create Date: 2021-05-20 11:01:20.824281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b35a36b589f8'
down_revision = '9030aa258427'
branch_labels = None
depends_on = None


def upgrade():
    # I know this is bad ;^;
    op.execute("INSERT INTO device (name) VALUES ('_no_device') ON CONFLICT DO NOTHING;")


def downgrade():
    pass
