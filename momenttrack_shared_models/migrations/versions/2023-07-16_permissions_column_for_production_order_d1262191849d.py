"""permissions_column_for_production_order

Revision ID: d1262191849d
Revises: 6f04bd30f5ce
Create Date: 2023-07-16 21:31:32.129846

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d1262191849d"
down_revision = "6f04bd30f5ce"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column(
        "production_order",
        sa.Column("public_view_permissions", sa.Integer(), nullable=True, default=0),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("production_order", "public_view_permissions")
    # ### end Alembic commands ###
