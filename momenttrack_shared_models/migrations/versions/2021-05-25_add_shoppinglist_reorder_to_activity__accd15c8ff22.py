"""add shoppinglist_reorder to activity type

Revision ID: accd15c8ff22
Revises: b827407344c9
Create Date: 2021-05-25 14:22:24.159796

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "accd15c8ff22"
down_revision = "b827407344c9"
branch_labels = None
depends_on = None

# Enum 'type' for PostgreSQL
enum_name = "activitytypeenum"
# Set temporary enum 'type' for PostgreSQL
tmp_enum_name = "tmp_" + enum_name

# Options for Enum
old_options = (
    "CHANGE_TRACK",
    "COMMENT",
    "LICENSE_PLATE_MOVE",
    "LICENSE_PLATE_MADEIT",
    "LICENSE_PLATE_DEDUCT",
)
new_option = "SHOPPINGLIST_REORDER"


new_options = sorted(old_options + (new_option,))
# Create enum fields
old_type = sa.Enum(*old_options, name=enum_name)
new_type = sa.Enum(*new_options, name=enum_name)


def upgrade():
    # prereq
    op.execute("ALTER TABLE activity DROP CONSTRAINT IF EXISTS " + enum_name)

    # Rename current enum type to tmp_
    op.execute("ALTER TYPE " + enum_name + " RENAME TO " + tmp_enum_name)
    # Create new enum type in db
    new_type.create(op.get_bind())
    # Update column to use new enum type
    op.execute(
        "ALTER TABLE activity ALTER COLUMN activity_type TYPE "
        + enum_name
        + " USING activity_type::text::"
        + enum_name
    )
    # Drop old enum type
    op.execute("DROP TYPE " + tmp_enum_name)


def downgrade():
    # Instantiate db query
    activity = sa.sql.table(
        "activity", sa.Column("activity_type", new_type, nullable=False)
    )
    # Convert new-opt to CHANGE_TRACK  (as a fallback)
    op.execute(
        activity.update()
        .where(activity.c.activity_type == "%s" % new_option)
        .values(activity_type="CHANGE_TRACK")
    )
    # Rename enum type to tmp_
    op.execute("ALTER TYPE " + enum_name + " RENAME TO " + tmp_enum_name)
    # Create enum type using old values
    old_type.create(op.get_bind())
    # Set enum type as type for activity_type column
    op.execute(
        "ALTER TABLE activity ALTER COLUMN activity_type TYPE "
        + enum_name
        + " USING activity_type::text::"
        + enum_name
    )
    # Drop temp enum type
    op.execute("DROP TYPE " + tmp_enum_name)
