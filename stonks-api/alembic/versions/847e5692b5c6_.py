"""empty message

Revision ID: 847e5692b5c6
Revises: 47b0a110e734
Create Date: 2021-04-18 21:43:46.578652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '847e5692b5c6'
down_revision = '47b0a110e734'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offer', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('offer', 'description')
    # ### end Alembic commands ###
