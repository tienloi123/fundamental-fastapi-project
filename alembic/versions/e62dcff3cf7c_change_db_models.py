"""Change db models

Revision ID: e62dcff3cf7c
Revises: 
Create Date: 2024-03-24 03:31:19.108210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e62dcff3cf7c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('stock_quantity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('total_price', sa.Float(), nullable=True),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('payment_method', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('author_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_title'), 'posts', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_posts_title'), table_name='posts')
    op.drop_table('posts')
    op.drop_table('payments')
    op.drop_table('orders')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    # ### end Alembic commands ###
