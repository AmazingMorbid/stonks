"""empty message

Revision ID: 399147180ee5
Revises: aff28f230617
Create Date: 2021-04-18 16:18:44.536399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '399147180ee5'
down_revision = 'aff28f230617'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fee_price',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fee_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Numeric(), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.ForeignKeyConstraint(['fee_id'], ['fee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('price')
    op.drop_constraint('fee_price_id_fkey', 'fee', type_='foreignkey')
    op.drop_column('fee', 'price_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fee', sa.Column('price_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('fee_price_id_fkey', 'fee', 'price', ['price_id'], ['id'])
    op.create_table('price',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('amount', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(length=3), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='price_pkey')
    )
    op.drop_table('fee_price')
    # ### end Alembic commands ###
