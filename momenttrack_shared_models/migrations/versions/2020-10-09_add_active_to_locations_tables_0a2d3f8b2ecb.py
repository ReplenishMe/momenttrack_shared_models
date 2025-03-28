"""add active to locations tables

Revision ID: 0a2d3f8b2ecb
Revises: 1dc29b9648d7
Create Date: 2020-10-09 22:13:22.399937

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0a2d3f8b2ecb"
down_revision = "1dc29b9648d7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "location",
        sa.Column("active", sa.Boolean(), server_default="1", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("location", "active")
    # ### end Alembic commands ###
