"""empty message

Revision ID: 6be99fd5e6b8
Revises: 1036bb106313
Create Date: 2023-01-29 20:54:15.916580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6be99fd5e6b8'
down_revision = '1036bb106313'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('linkedin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=160), nullable=True),
    sa.Column('about', sa.String(length=32), nullable=True),
    sa.Column('network_name', sa.String(length=16), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('links_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['links_id'], ['links.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('linkedin')
    # ### end Alembic commands ###