"""add wms tables

Revision ID: d49ba843b5d9
Revises: 83eb5aac5793
Create Date: 2020-12-23 15:25:54.561976

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d49ba843b5d9"
down_revision = "83eb5aac5793"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "location", sa.Column("location_type", sa.String(length=63), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("location", "location_type")
    # ### end Alembic commands ###