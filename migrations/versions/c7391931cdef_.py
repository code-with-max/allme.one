"""empty message

Revision ID: c7391931cdef
Revises: 3d69f59f1e3e
Create Date: 2023-02-09 19:36:18.398736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7391931cdef'
down_revision = '3d69f59f1e3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('steamdeveloper',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=160), nullable=True),
    sa.Column('about', sa.String(length=32), nullable=True),
    sa.Column('network_name', sa.String(length=16), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('links_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['links_id'], ['links.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('steampublisher',
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
    op.drop_table('steampublisher')
    op.drop_table('steamdeveloper')
    # ### end Alembic commands ###