"""init

Revision ID: 8a6f19d30c1a
Revises: 
Create Date: 2023-04-21 22:09:13.132156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a6f19d30c1a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('card_status',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime),
                    sa.PrimaryKeyConstraint('id')

                    )
    op.create_table('visible_status',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('last_name', sa.String()),
                    sa.Column('mail', sa.String(), nullable=False),
                    sa.Column('password_hash', sa.String()),
                    sa.Column('created_at', sa.DateTime),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('service',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('status', sa.Integer, nullable=False),
                    sa.Column('short_deskription', sa.String()),
                    sa.Column('created_at', sa.DateTime),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(
                        ['status'], ['visible_status.id'], ),
                    )
    op.create_table('client_request',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('phone', sa.String(), nullable=False),
                    sa.Column('mail', sa.String(), nullable=False),
                    sa.Column('message', sa.String(),  nullable=False),
                    sa.Column('theme', sa.Integer()),
                    sa.Column('status', sa.Integer()),
                    sa.Column('executor', sa.Integer()),
                    sa.Column('created_at', sa.DateTime),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(
                        ['theme'], ['service.id'], ),
                    sa.ForeignKeyConstraint(
                        ['status'], ['card_status.id'], ),
                    sa.ForeignKeyConstraint(
                        ['executor'], ['users.id'], ),
                    )
    op.create_table('image',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('url', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('news',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('header', sa.String(), nullable=False),
                    sa.Column('body', sa.String(), nullable=False),
                    sa.Column('status', sa.Integer, nullable=False),
                    sa.Column('created_at', sa.DateTime),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(
                        ['status'], ['visible_status.id'], ),
                    )
    op.create_table('services_img',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('service_id', sa.Integer, nullable=False),
                    sa.Column('image_id', sa.Integer, nullable=False),
                    sa.Column('created_at', sa.DateTime),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(
                        ['service_id'], ['service.id'], ),
                    sa.ForeignKeyConstraint(
                        ['image_id'], ['image.id'], ),
                    )
    op.create_table('news_img',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('news_id', sa.Integer, nullable=False),
                    sa.Column('image_id', sa.Integer, nullable=False),
                    sa.Column('created_at', sa.DateTime),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(
                        ['news_id'], ['news.id'], ),
                    sa.ForeignKeyConstraint(
                        ['image_id'], ['image.id'], ),
                    )


def downgrade() -> None:
    op.drop_table('news_img')
    op.drop_table('services_img')
    op.drop_table('news')
    op.drop_table('image')
    op.drop_table('client_request')
    op.drop_table('service')
    op.drop_table('users')
    op.drop_table('visible_status')
    op.drop_table('card_status')
