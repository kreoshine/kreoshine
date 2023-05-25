"""initial

Revision ID: 5bd479fca81b
Revises: 
Create Date: 2023-05-25 12:24:36.520974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bd479fca81b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client_requests',
    sa.Column('client_request_uid', sa.UUID()),
    sa.Column('client_name', sa.String()),
    sa.Column('client_phone', sa.String(), nullable=True),
    sa.Column('client_mail', sa.String()),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('tittle', sa.String(), nullable=True),
    sa.Column('request_status', sa.String()),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('client_request_uid')
    )
    op.create_table('trade_items',
    sa.Column('trade_item_uid', sa.UUID()),
    sa.Column('name', sa.String()),
    sa.Column('description', sa.String()),
    sa.Column('short_description', sa.String()),
    sa.Column('is_visible', sa.Boolean()),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('trade_item_uid')
    )
    op.create_table('users',
    sa.Column('user_uid', sa.UUID()),
    sa.Column('first_name', sa.String()),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('mail', sa.String()),
    sa.Column('password_hash', sa.String()),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('user_uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('trade_items')
    op.drop_table('client_requests')
    # ### end Alembic commands ###
