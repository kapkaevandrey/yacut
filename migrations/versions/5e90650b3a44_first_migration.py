"""First migration

Revision ID: 5e90650b3a44
Revises: 
Create Date: 2022-05-03 22:39:38.068675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e90650b3a44'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('URL_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original', sa.String(length=2048), nullable=False),
    sa.Column('short', sa.String(length=16), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short')
    )
    op.create_index(op.f('ix_URL_map_timestamp'), 'URL_map', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_URL_map_timestamp'), table_name='URL_map')
    op.drop_table('URL_map')
    # ### end Alembic commands ###