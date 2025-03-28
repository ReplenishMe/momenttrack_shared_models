"""Add uom to product

Revision ID: 4171f227a4c7
Revises: 6513cf6599fc
Create Date: 2021-02-24 23:40:47.298833

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4171f227a4c7"
down_revision = "6513cf6599fc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("product", sa.Column("uom", sa.String(length=31), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("product", "uom")
    # ### end Alembic commands ###
