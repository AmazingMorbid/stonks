"""empty message

Revision ID: cdfabc4ac843
Revises: 85c1674f6b9b
Create Date: 2021-04-19 21:17:08.570070

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cdfabc4ac843'
down_revision = '85c1674f6b9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offer',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('category', sa.String(length=32), nullable=False),
    sa.Column('price', sa.Numeric(precision=15, scale=4), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('photos', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('last_refresh_time', sa.DateTime(), nullable=True),
    sa.Column('last_scraped_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('delivery',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('offer_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('price', sa.Numeric(precision=15, scale=4), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stonks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('offer_id', sa.String(), nullable=False),
    sa.Column('low_price', sa.Numeric(precision=15, scale=4), nullable=False),
    sa.Column('high_price', sa.Numeric(precision=15, scale=4), nullable=False),
    sa.Column('average_price', sa.Numeric(precision=15, scale=4), nullable=False),
    sa.Column('median_price', sa.Numeric(precision=15, scale=4), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fee',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stonks_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=15, scale=4), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['stonks_id'], ['stonks.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fee')
    op.drop_table('stonks')
    op.drop_table('delivery')
    op.drop_table('offer')
    # ### end Alembic commands ###
