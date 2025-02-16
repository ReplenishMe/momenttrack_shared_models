from ..model_mixins import (
    IdMixin,
    TimestampMixin,
    BelongsToOrgMixin
)
from ..models import Role, User
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type
from ...extensions import db
from ...utils import (
    generate_token,
    SerializableEnum
)


class Organization(db.BaseModel, IdMixin, TimestampMixin):
    """company details"""

    # Profile info
    name = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128), unique=True, nullable=False)
    code = db.Column(
        db.String(50), unique=True,
        default=lambda: generate_token(5)
    )
    address = db.Column(db.Text())
    order_template = db.Column(
        mutable_json_type(
            dbtype=JSONB,
            nested=True
        )
    )

    users = db.relationship("User", backref="organization")
    roles = db.relationship("Role", lazy="dynamic")

    def has_user(self, email):
        return self.users.filter(User.email == email).count() == 1

    @classmethod
    def get_by_slug(cls, slug):
        return cls.query.filter(cls.slug == slug).first()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter(cls.id == _id).one()

    @property
    def default_role(self):
        return self.roles.filter(
            Role.name == "default", Role.role_type == Role.BUILTIN_GROUP
        ).first()

    @property
    def admin_role(self):
        return self.roles.filter(
            Role.name == "admin", Role.role_type == Role.BUILTIN_GROUP
        ).first()


class VirtualERPTransactionStatus(SerializableEnum):
    RECEIVED = "RECEIVED"
    PAIRED = "PAIRED"


class VirtualERP(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    color_code = db.Column(db.String())
    item_id = db.Column(db.String())
    item_num = db.Column(db.String())
    item_sales_id = db.Column(db.String())
    job_name = db.Column(db.String())
    masking_batch = db.Column(db.String(127))
    masking_qr = db.Column(db.String(63))
    pur_batch = db.Column(db.String(127))
    pur_qr = db.Column(db.String(63))
    pvc_batch = db.Column(db.String(127))
    pvc_qr = db.Column(db.String(63))
    sales_order = db.Column(db.String(127))
    transaction_status = db.Column(
        db.Enum(VirtualERPTransactionStatus),
        default=VirtualERPTransactionStatus.RECEIVED
    )
    license_plate_id = db.Column(db.Integer, db.ForeignKey('license_plate.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
