"""table_01

Revision ID: a83ea16f9232
Revises: 2f439bb600f1
Create Date: 2023-04-23 19:48:09.232501

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a83ea16f9232'
down_revision = '2f439bb600f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('card_status', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('client_request', 'theme',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('client_request', 'status',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('client_request', 'executor',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('client_request', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('image', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('news', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('news_img', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('service', 'short_deskription',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('service', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('services_img', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'password_hash',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('visible_status', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('visible_status', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('users', 'password_hash',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('services_img', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('service', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('service', 'short_deskription',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('news_img', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('news', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('image', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('client_request', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('client_request', 'executor',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('client_request', 'status',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('client_request', 'theme',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('card_status', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
