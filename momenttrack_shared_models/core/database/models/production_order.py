from ..model_mixins import (
    BelongsToOrgMixin, IdMixin,
    TimestampMixin
)
from ...extensions import db
from ...utils import generate_uuid
from .product import Product
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type
from ...utils import SerializableEnum


class ProductionOrderStatusEnum(SerializableEnum):
    CREATED = "CREATED"
    ONHOLD = "ONHOLD"
    DELETED = "DELETED"


class ProductionOrder(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """Production Order table"""

    # __table_args__ = (
    #     db.UniqueConstraint('organization_id', 'name'),
    # )

    location_id = db.Column(
        db.Integer,
        db.ForeignKey("location.id"),
        comment="Current facility id",
        default=None,
        nullable=True,
    )
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    requested_qty = db.Column(db.Float())

    planned_start_date = db.Column(db.DateTime(), default=None)
    planned_end_date = db.Column(db.DateTime(), default=None)

    actual_start_date = db.Column(db.DateTime(), default=None)
    actual_end_date = db.Column(db.DateTime(), default=None)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(
        db.Enum(ProductionOrderStatusEnum, native_enum=True, length=31),
        nullable=False,
        default=ProductionOrderStatusEnum.CREATED,
    )
    order_template = db.Column(
        mutable_json_type(
            dbtype=JSONB,
            nested=True
        )
    )

    docid = db.Column(
        db.String(63), nullable=True, unique=True, default=lambda: generate_uuid()
    )

    external_docid = db.Column(db.String(63), nullable=True, default=None)
    redirect_url = db.Column(db.String(127), default=None)

    # relations
    production_order_lineitems = db.relationship(
        "ProductionOrderLineitem", backref="production_order", lazy="dynamic"
    )

    # dynamic
    user = db.relationship("User", backref="production_order", lazy="joined")
    product = db.relationship("Product", backref="production_order", lazy="joined")
    public_view_permissions = db.Column(db.Integer, default=2)

    @classmethod
    def get_by_docid_and_org(cls, docid, org):
        return cls.get_by_org(org).filter(cls.docid == docid).first()

    def edit_pub_view_perms(self, add=[], remove=[]):
        if not self.public_view_permissions:
            self.public_view_permissions = 2
        for perm in add:
            if not self.has_perm(perm):
                self.public_view_permissions += perm
        for perm in remove:
            if self.has_perm(perm):
                self.public_view_permissions -= perm

    @classmethod
    def get_system_order(cls, org, user_id):
        system_product = Product.get_system_product(org)
        order = cls.get_by_org(org).filter(
            cls.requested_qty == '+infinity',
            cls.product_id == system_product.id
        ).first()
        if not order:
            order = cls(
                organization_id=org,
                product_id=system_product.id,
                requested_qty='+infinity',
                user_id=user_id
            )
            db.writer_session.add(order)
            db.writer_session.commit()
        return order

    def has_perm(self, perm):
        return self.public_view_permissions & perm == perm
