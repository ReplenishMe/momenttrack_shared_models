from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db
from ...utils import generate_uuid
from ...utils import SerializableEnum


class PickStatusEnum(SerializableEnum):
    CREATED = "CREATED"
    DELETED = "DELETED"


class PickTypeEnum(SerializableEnum):
    WORKORDER = "WORKORDER"
    PRODUCTIONORDER = "PRODUCTIONORDER"


class Pick(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """WMS: pick table"""

    # __table_args__ = (
    #     db.UniqueConstraint('organization_id', 'name'),
    # )

    # @TODO make this false
    docid = db.Column(
        db.String(63), nullable=True, unique=True, default=lambda: generate_uuid()
    )
    pick_type = db.Column(
        db.Enum(PickTypeEnum, native_enum=True, length=31),
        nullable=False,
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("location.id"), comment="Current facility id"
    )
    dest_location_id = db.Column(
        db.Integer, db.ForeignKey("location.id"), comment="Destination facility id"
    )
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # source_id = db.Column(db.Integer, db.ForeignKey("pick.id"))
    # target_id = db.Column(db.Integer, db.ForeignKey("pick.id"))

    # status = db.Column(db.String(31), nullable=False, default="CREATED")
    status = db.Column(
        db.Enum(PickStatusEnum, native_enum=True, length=31),
        nullable=False,
        default=PickStatusEnum.CREATED,
    )

    planned_start_date = db.Column(db.DateTime(), default=None)
    planned_end_date = db.Column(db.DateTime(), default=None)

    actual_start_date = db.Column(db.DateTime(), default=None)
    actual_end_date = db.Column(db.DateTime(), default=None)

    external_docid = db.Column(db.String(63), nullable=True, default=None)
    redirect_url = db.Column(db.String(127), default=None)

    # status = db.Column(db.Enum(PickStatusEnum), nullable=False, default=PickStatusEnum.CREATED)

    # relations
    pick_lineitems = db.relationship("PickLineitem", backref="pick", lazy="dynamic")
    user = db.relationship("User", backref="pick", lazy="joined")

    @classmethod
    def get_by_docid_and_org(cls, docid, org):
        return cls.get_by_org(org).filter(cls.docid == docid).first()
