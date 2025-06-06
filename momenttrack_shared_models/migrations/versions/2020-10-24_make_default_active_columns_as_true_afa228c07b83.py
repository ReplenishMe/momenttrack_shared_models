"""make default active columns as True

Revision ID: afa228c07b83
Revises: 7a73ee113025
Create Date: 2020-10-24 09:47:28.433299

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "afa228c07b83"
down_revision = "7a73ee113025"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("bin", "bin_family_id", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column(
        "bin", "organization_id", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("bin", "organization_id", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("bin", "bin_family_id", existing_type=sa.INTEGER(), nullable=True)
    # ### end Alembic commands ###
