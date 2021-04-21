"""empty message

Revision ID: 5de697906da7
Revises: 0c328b78769a
Create Date: 2021-04-18 21:48:43.619939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5de697906da7'
down_revision = '0c328b78769a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('delivery',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('offer_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('price', sa.Numeric(precision=4), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['offer_id'], ['offer.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('delivery')
    # ### end Alembic commands ###
