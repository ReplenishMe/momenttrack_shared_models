from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db
from ...utils import generate_token
from ...utils import SerializableEnum


class LicensePlateStatusEnum(SerializableEnum):
    CREATED = "CREATED"
    RETIRED = "RETIRED"
    DELETED = "DELETED"


class LicensePlate(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """WMS: License plate table"""

    # __table_args__ = (
    #     db.UniqueConstraint('organization_id', 'name'),
    # )

    lp_id = db.Column(
        db.String(63),
        nullable=False,
        unique=True,
        default=lambda: generate_token(25)
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )
    quantity = db.Column(db.Float(), nullable=False)
    # remaining_qty = db.Column(db.Float())
    organization_id = db.Column(
        db.Integer(),
        db.ForeignKey("organization.id"),
        nullable=False
    )
    location_id = db.Column(
        db.Integer,
        db.ForeignKey("location.id"),
        nullable=False
    )
    parent_license_plate_id = db.Column(
        db.Integer,
        db.ForeignKey("license_plate.id"),
        nullable=True
    )
    external_serial_number = db.Column(db.String(127))
    # @TODO Make it non-nullable
    is_consumer_facing = db.Column(db.Boolean(), nullable=True, default=False)
    redirect_url = db.Column(db.String(127), default=None)

    # status = db.Column(db.String(31), nullable=False, default="CREATED")
    status = db.Column(
        db.Enum(LicensePlateStatusEnum, native_enum=True, length=31),
        nullable=False,
        default=LicensePlateStatusEnum.CREATED,
    )
    container_id = db.Column(
        db.Integer,
        db.ForeignKey('container.id'),
        index=True
    )
    lineitems = db.relationship(
        'ProductionOrderLineitem', backref='license_plate'
    )

    @classmethod
    def get_by_lp_id_and_org(cls, lp_id, org, fetch_all=False, session=None):
        if session:
            lp = cls.get_by_org(org, session=session).filter(
                cls.lp_id == lp_id
            )
        else:
            lp = cls.get_by_org(org).filter(cls.lp_id == lp_id)
        if fetch_all:
            return lp.all()
        return lp.first()

    @classmethod
    def get_by_lp_id_or_id_and_org(cls, _id, org, session=None):
        if isinstance(_id, str):
            return cls.get_by_lp_id_and_org(_id, org, session=session)
        elif isinstance(_id, int):
            return cls.get_by_id_and_org(_id, org, session=session)

    @classmethod
    def get_by_id(cls, id, fetch_all=False, session=None):
        if session:
            lp = cls.query.with_session(session).filter(cls.id == id)
        else:
            lp = query = cls.query.filter(cls.id == id)
        if fetch_all:
            return lp.all()
        return lp.first()

    @classmethod
    def get_by_external_serial_number_and_org(
        cls, external_serial_number, org, fetch_all=False
    ):
        lp = cls.get_by_org(org).filter(
            cls.external_serial_number == external_serial_number
        )
        if fetch_all:
            return lp.all()
        return lp.first()

    @classmethod
    def get_by_external_serial_number_contains_and_org(
        cls, external_serial_number, org, fetch_all=False
    ):
        lp = cls.get_by_org(org).filter(
            cls.external_serial_number.contains(external_serial_number)
        )
        if fetch_all:
            return lp.all()
        return lp.first()

    @classmethod
    def fetch_all_by_location_and_org(
        cls, location_id, org, fetch_all=True, session=None
    ):
        if session:
            lps = cls.get_by_org(org, session=session).filter(
                cls.location_id == location_id
            )
            if not fetch_all:
                return lps.first()
            return lps.all()
        else:
            lps = cls.get_by_org(org).filter(cls.location_id == location_id)
            if not fetch_all:
                return lps.first()
            return lps.all()
