"""бронирование столов

Revision ID: e5e807c73292
Revises: 3e9c681ae437
Create Date: 2025-05-13 17:01:13.385104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5e807c73292'
down_revision: Union[str, None] = '3e9c681ae437'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('tables')
    op.drop_table('user_reviews')
    op.drop_table('order_items')
    op.drop_table('time_slots')
    op.drop_table('reserv')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reserv',
    sa.Column('reserv_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('count_people', sa.INTEGER(), nullable=False),
    sa.Column('table_id', sa.INTEGER(), nullable=False),
    sa.Column('reserv_date', sa.DATE(), nullable=False),
    sa.Column('time_id', sa.INTEGER(), nullable=False),
    sa.Column('status_r', sa.VARCHAR(length=9), nullable=False),
    sa.ForeignKeyConstraint(['table_id'], ['tables.table_id'], ),
    sa.ForeignKeyConstraint(['time_id'], ['time_slots.slot_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('reserv_id')
    )
    op.create_table('time_slots',
    sa.Column('slot_id', sa.INTEGER(), nullable=False),
    sa.Column('date', sa.DATE(), nullable=False),
    sa.Column('start', sa.TIME(), nullable=False),
    sa.Column('end', sa.TIME(), nullable=False),
    sa.PrimaryKeyConstraint('slot_id')
    )
    op.create_table('order_items',
    sa.Column('item_id', sa.INTEGER(), nullable=False),
    sa.Column('item_order_id', sa.INTEGER(), nullable=False),
    sa.Column('item_prod_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['item_order_id'], ['orders.o_id'], ),
    sa.ForeignKeyConstraint(['item_prod_id'], ['products.prod_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_table('user_reviews',
    sa.Column('review_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('product_id', sa.INTEGER(), nullable=False),
    sa.Column('rating', sa.INTEGER(), nullable=False),
    sa.Column('comment', sa.TEXT(), nullable=True),
    sa.Column('created_comment', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.prod_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('review_id')
    )
    op.create_table('tables',
    sa.Column('table_id', sa.INTEGER(), nullable=False),
    sa.Column('table_number', sa.VARCHAR(length=10), nullable=False),
    sa.Column('table_price', sa.NUMERIC(precision=10, scale=2), nullable=False),
    sa.Column('img_table', sa.TEXT(), nullable=True),
    sa.Column('seating_capacity', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('table_id')
    )
    op.create_table('orders',
    sa.Column('o_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('o_sum', sa.NUMERIC(precision=10, scale=2), nullable=False),
    sa.Column('o_status', sa.VARCHAR(length=14), nullable=False),
    sa.Column('o_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('o_id')
    )
    # ### end Alembic commands ###
