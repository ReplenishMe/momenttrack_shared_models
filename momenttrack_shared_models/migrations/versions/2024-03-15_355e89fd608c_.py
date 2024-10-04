"""empty message

Revision ID: 355e89fd608c
Revises: 319e0c93f1af
Create Date: 2024-03-14 23:29:10.656793

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '355e89fd608c'
down_revision = '319e0c93f1af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stack',
    sa.Column('stack_id', sa.String(length=63), nullable=False),
    sa.Column('part_number', sa.String(length=63), nullable=False),
    sa.Column('production_order_id', sa.String(length=63), nullable=False),
    sa.Column('status', sa.Enum('OPEN', 'CLOSED', name='stackstatusenum', length=31), nullable=False),
    sa.Column('item_count', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('stack_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    
    op.drop_table('stack')
    op.execute('DROP TYPE IF EXISTS stackstatusenum;')
    # ### end Alembic commands ###
