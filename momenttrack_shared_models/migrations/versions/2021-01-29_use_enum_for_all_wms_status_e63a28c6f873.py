"""use enum for all wms status

Revision ID: e63a28c6f873
Revises: f6f82d96f180
Create Date: 2021-01-29 02:05:07.562108

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e63a28c6f873"
down_revision = "f6f82d96f180"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "license_plate_move", sa.Column("user_id", sa.Integer(), nullable=True)
    )
    op.alter_column(
        "license_plate_move",
        "license_plate_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "license_plate_move", "product_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.create_foreign_key(None, "license_plate_move", "user", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "license_plate_move", type_="foreignkey")
    op.alter_column(
        "license_plate_move", "product_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "license_plate_move",
        "license_plate_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.drop_column("license_plate_move", "user_id")
    # ### end Alembic commands ###