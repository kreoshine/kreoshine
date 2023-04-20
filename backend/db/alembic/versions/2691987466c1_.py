"""empty message

Revision ID: 2691987466c1
Revises: 
Create Date: 2023-04-20 20:09:36.261898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2691987466c1'
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


def downgrade() -> None:
    op.drop_table('card_status')
