"""empty message

Revision ID: 1053475814e3
Revises: de31857180d1
Create Date: 2021-04-18 21:27:02.242298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1053475814e3'
down_revision = 'de31857180d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offer', sa.Column('id_in_store', sa.String(), nullable=False))
    op.drop_column('offer', 'store_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offer', sa.Column('store_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('offer', 'id_in_store')
    # ### end Alembic commands ###
