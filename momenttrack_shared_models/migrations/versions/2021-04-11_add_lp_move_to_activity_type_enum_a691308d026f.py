"""add lp_move to activity type enum

Revision ID: a691308d026f
Revises: 487fb7b64f8b
Create Date: 2021-04-11 00:40:08.150635

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a691308d026f"
down_revision = "487fb7b64f8b"
branch_labels = None
depends_on = None


# Enum 'type' for PostgreSQL
enum_name = "activitytypeenum"
# Set temporary enum 'type' for PostgreSQL
tmp_enum_name = "tmp_" + enum_name

# Options for Enum
old_options = ("CHANGE_TRACK", "COMMENT")
new_options = sorted(old_options + ("LICENSE_PLATE_MOVE",))

# Create enum fields
old_type = sa.Enum(*old_options, name=enum_name)
new_type = sa.Enum(*new_options, name=enum_name)


def upgrade():
    # prereq
    op.execute("ALTER TABLE activity DROP CONSTRAINT " + enum_name)

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
    # Convert LICENSE_PLATE_MOVE to CHANGE_TRACK  (as a fallback)
    op.execute(
        activity.update()
        .where(activity.c.activity_type == "LICENSE_PLATE_MOVE")
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
