"""make enums native

Revision ID: 0a7b594b2f8a
Revises: 0137efae8ef3
Create Date: 2021-03-08 18:48:19.840275

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# REF::: https://github.com/sqlalchemy/alembic/issues/278#issuecomment-668238745
# REF2::: https://markrailton.com/blog/creating-migrations-when-changing-an-enum-in-python-using-sql-alchemy

# revision identifiers, used by Alembic.
revision = "0a7b594b2f8a"
down_revision = "0137efae8ef3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    activitytypeenum = postgresql.ENUM(
        "CHANGE_TRACK", "COMMENT", name="activitytypeenum"
    )
    activitytypeenum.create(op.get_bind())

    activitychangetrackfieldtypeenum = postgresql.ENUM(
        "INTEGER",
        "FLOAT",
        "STRING",
        "DATETIME",
        name="activitychangetrackfieldtypeenum",
    )
    activitychangetrackfieldtypeenum.create(op.get_bind())
    op.alter_column(
        "activity_change_track",
        "field_type",
        existing_type=sa.VARCHAR(length=8),
        type_=activitychangetrackfieldtypeenum,
        existing_comment="column data type",
        existing_nullable=False,
        postgresql_using="field_type::activitychangetrackfieldtypeenum",
    )

    licenseplatestatusenum = postgresql.ENUM(
        "CREATED", "RETIRED", "DELETED", name="licenseplatestatusenum"
    )
    licenseplatestatusenum.create(op.get_bind())
    op.alter_column(
        "license_plate",
        "status",
        existing_type=sa.VARCHAR(length=31),
        type_=licenseplatestatusenum,
        existing_nullable=False,
        postgresql_using="status::licenseplatestatusenum",
    )

    licenseplatemovestatusenum = postgresql.ENUM(
        "CREATED", "DELETED", name="licenseplatemovestatusenum"
    )
    licenseplatemovestatusenum.create(op.get_bind())
    op.alter_column(
        "license_plate_move",
        "status",
        existing_type=sa.VARCHAR(length=31),
        type_=licenseplatemovestatusenum,
        existing_nullable=False,
        postgresql_using="status::licenseplatemovestatusenum",
    )

    picktypeenum = postgresql.ENUM("WORKORDER", "PRODUCTIONORDER", name="picktypeenum")
    picktypeenum.create(op.get_bind())
    op.alter_column(
        "pick",
        "pick_type",
        existing_type=sa.VARCHAR(length=31),
        type_=picktypeenum,
        existing_nullable=False,
        postgresql_using="pick_type::picktypeenum",
    )

    pickstatusenum = postgresql.ENUM("CREATED", "DELETED", name="pickstatusenum")
    pickstatusenum.create(op.get_bind())
    op.alter_column(
        "pick",
        "status",
        existing_type=sa.VARCHAR(length=7),
        type_=pickstatusenum,
        existing_nullable=False,
        postgresql_using="status::pickstatusenum",
    )

    picklineitemstatusenum = postgresql.ENUM(
        "CREATED", "DRAFT", "DONE", "DELETED", name="picklineitemstatusenum"
    )
    picklineitemstatusenum.create(op.get_bind())
    op.alter_column(
        "pick_lineitem",
        "status",
        existing_type=sa.VARCHAR(length=7),
        type_=picklineitemstatusenum,
        existing_nullable=False,
        postgresql_using="status::picklineitemstatusenum",
    )

    userstatusenum = postgresql.ENUM(
        "UNCONFIRMED", "ACTIVE", "DELETED", name="userstatusenum"
    )
    userstatusenum.create(op.get_bind())
    op.alter_column(
        "user",
        "status",
        existing_type=sa.VARCHAR(length=11),
        type_=userstatusenum,
        existing_nullable=False,
        postgresql_using="status::userstatusenum",
    )

    op.add_column(
        "product",
        sa.Column(
            "is_external",
            sa.Boolean(),
            nullable=True,
            comment="Whether the product is external to momenttrack (no tracking will be available for this)",
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user",
        "status",
        existing_type=sa.Enum(
            "UNCONFIRMED", "ACTIVE", "DELETED", name="userstatusenum"
        ),
        type_=sa.VARCHAR(length=11),
        existing_nullable=False,
    )
    op.drop_column("product", "is_external")
    op.alter_column(
        "pick_lineitem",
        "status",
        existing_type=sa.Enum(
            "CREATED", "DRAFT", "DONE", "DELETED", name="picklineitemstatusenum"
        ),
        type_=sa.VARCHAR(length=7),
        existing_nullable=False,
    )
    op.alter_column(
        "pick",
        "status",
        existing_type=sa.Enum("CREATED", "DELETED", name="pickstatusenum"),
        type_=sa.VARCHAR(length=7),
        existing_nullable=False,
    )
    op.alter_column(
        "pick",
        "pick_type",
        existing_type=sa.Enum("WORKORDER", "PRODUCTIONORDER", name="picktypeenum"),
        type_=sa.VARCHAR(length=31),
        existing_nullable=False,
    )
    op.alter_column(
        "license_plate_move",
        "status",
        existing_type=sa.Enum("CREATED", "DELETED", name="licenseplatemovestatusenum"),
        type_=sa.VARCHAR(length=31),
        existing_nullable=False,
    )
    op.alter_column(
        "license_plate",
        "status",
        existing_type=sa.Enum(
            "CREATED", "RETIRED", "DELETED", name="licenseplatestatusenum"
        ),
        type_=sa.VARCHAR(length=31),
        existing_nullable=False,
    )
    op.alter_column(
        "activity_change_track",
        "field_type",
        existing_type=sa.Enum(
            "INTEGER",
            "FLOAT",
            "STRING",
            "DATETIME",
            name="activitychangetrackfieldtypeenum",
        ),
        type_=sa.VARCHAR(length=8),
        existing_comment="column data type",
        existing_nullable=False,
    )
    # op.alter_column(
    #     "activity",
    #     "activity_type",
    #     existing_type=sa.Enum("CHANGE_TRACK", "COMMENT", name="activitytypeenum"),
    #     type_=sa.VARCHAR(length=12),
    #     nullable=True,
    # )

    # drop the created types
    op.execute("DROP TYPE activitytypeenum;")
    op.execute("DROP TYPE activitychangetrackfieldtypeenum;")
    op.execute("DROP TYPE licenseplatestatusenum;")
    op.execute("DROP TYPE licenseplatemovestatusenum;")
    op.execute("DROP TYPE picktypeenum;")
    op.execute("DROP TYPE pickstatusenum;")
    op.execute("DROP TYPE picklineitemstatusenum;")
    op.execute("DROP TYPE userstatusenum;")

    # ### end Alembic commands ###