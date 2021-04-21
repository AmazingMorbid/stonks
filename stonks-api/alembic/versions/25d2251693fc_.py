"""empty message

Revision ID: 25d2251693fc
Revises: 1ac5dda85e68
Create Date: 2021-04-18 22:14:09.572671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25d2251693fc'
down_revision = '1ac5dda85e68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stonks', sa.Column('average_price', sa.Numeric(precision=4), nullable=False))
    op.add_column('stonks', sa.Column('high_price', sa.Numeric(precision=4), nullable=False))
    op.add_column('stonks', sa.Column('low_price', sa.Numeric(precision=4), nullable=False))
    op.add_column('stonks', sa.Column('median_price', sa.Numeric(precision=4), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stonks', 'median_price')
    op.drop_column('stonks', 'low_price')
    op.drop_column('stonks', 'high_price')
    op.drop_column('stonks', 'average_price')
    # ### end Alembic commands ###
