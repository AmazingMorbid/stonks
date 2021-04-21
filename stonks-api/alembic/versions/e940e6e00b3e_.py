"""empty message

Revision ID: e940e6e00b3e
Revises: 9ec0c8524fad
Create Date: 2021-04-18 17:14:26.735589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e940e6e00b3e'
down_revision = '9ec0c8524fad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stonks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('offer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fee',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stonks_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=4), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['stonks_id'], ['stonks.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fee')
    op.drop_table('stonks')
    op.drop_table('store')
    op.drop_table('offer')
    # ### end Alembic commands ###
