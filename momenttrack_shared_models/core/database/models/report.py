from dataclasses import dataclass

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, and_, func

from ..models import LicensePlate
from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db


class EverythingReport(
    db.BaseModel, IdMixin,
    TimestampMixin, BelongsToOrgMixin
):
    quantity = db.Column(db.Integer)
    external_serial_number = db.Column(db.String(127))
    lp_id = db.Column(db.String(63), nullable=False, unique=True, index=True)
    status = db.Column(db.String)
    product_id = db.Column(db.Integer)
    beacon_id = db.Column(db.String(11), index=True)
    location_name = db.Column(db.String(63))
    part_number = db.Column(db.String(31))
    description = db.Column(db.String(255))
    intake_date = db.Column(db.DateTime)
    location_width = db.Column(db.Float)
    location_depth = db.Column(db.Float)
    location_height = db.Column(db.Float)
    category = db.Column(db.String)
    who_moved_last = db.Column(db.String)
    when_last_movement = db.Column(db.DateTime)
    last_interaction = db.Column(db.DateTime)
    production_order_id = db.Column(db.String(63))
    organization_id = db.Column(db.Integer(), index=True)

    @classmethod
    def get_by_license_plate_id(cls, lp_id, session=None):
        stmt = select(cls).where(cls.lp_id == lp_id)
        if session:
            return session.scalars(stmt).first()
        return db.session.scalars(stmt).first()

    @classmethod
    def upsert(cls, payload, session=None):
        report_raw = payload['report_raw']
        stmt = insert(cls).values(**report_raw)
        stmt = stmt.on_conflict_do_update(
            index_elements=['lp_id'],
            set_=report_raw
        )
        session.execute(stmt)


@dataclass
class EverythingReportResp:
    new_object: EverythingReport = None
    is_new: bool = False


class LineItemTotals(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    __table_args__ = (db.UniqueConstraint("location_id", "production_order_id"),)
    organization_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String)
    production_order_id = db.Column(db.Integer, index=True)
    total_items = db.Column(db.Integer)
    location_id = db.Column(db.Integer)

    @classmethod
    def get_by_id(cls, object_id, session=None):
        stmt = select(cls).where(cls.id == object_id)
        if session:
            return session.scalar(stmt)
        return db.session.scalar(stmt)

    @classmethod
    def get_by_org(cls, org_id, session=None):
        stmt = select(cls).where(cls.organization_id == org_id)
        if session:
            return session.scalars(stmt).all()
        return db.session.scalars(stmt).all()

    @classmethod
    def get_by_order(cls, order_id, session=None):
        stmt = select(cls).where(cls.production_order_id == order_id)
        if session:
            return session.scalars(stmt).all()
        return db.session.scalars(stmt).all()

    @classmethod
    def get_by_location_and_order(cls, loc_id, order_id, session=None):
        stmt = select(cls).where(
            and_(
                cls.location_id == loc_id,
                cls.production_order_id == order_id
            )
        )
        if session:
            return session.scalars(stmt).first()
        return db.session.scalars(stmt).first()

    @classmethod
    def upsert(cls, payload, session=None):
        po_id = payload['production_order_id']
        location = payload['location']
        stmt = insert(cls).values(
            production_order_id=po_id,
            location_id=location.id,
            organization_id=location.organization_id,
            name=location.name,
            total_items=1  # Default value if row is created
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=['location_id', 'production_order_id'],
            set_={
                'total_items': cls.total_items + 1,
                'name': stmt.excluded.name
            }
        )
        session.execute(stmt)


@dataclass
class LineItemTotalsResp:
    totals_object: LineItemTotals = None
    is_new: bool = False


@dataclass
class ReportResp:
    new_object = None
    is_new: bool = False


class LineGraphData(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    __table_args__ = (db.UniqueConstraint("location_id", "product_id", "date_key"),)
    organization_id = db.Column(db.Integer, index=True)
    date = db.Column(db.DateTime)
    date_key = db.Column(db.String, index=True)
    quantity = db.Column(db.Integer)
    location_id = db.Column(db.Integer, index=True)
    part_number = db.Column(db.String, index=True)
    product_id = db.Column(db.Integer, index=True)

    @classmethod
    def get_by_date_key_location_id_and_prod_id(
        cls, loc_id, date_key, prod_id, session=None
    ):
        stmt = select(cls).where(
            and_(
                cls.location_id == loc_id,
                cls.date_key == date_key,
                cls.product_id == prod_id
            )
        )
        if session:
            return session.scalars(stmt).first()
        return db.session.scalars(stmt).first()

    @classmethod
    def upsert(cls, payload, session=None):
        loc_id = payload['loc_id']
        date_key = payload['date_key']
        lp_move = payload['lp_move']
        prod = payload['product']
        stmt = insert(cls).values(
            date=lp_move.created_at,
            date_key=date_key,
            quantity=1,
            organization_id=lp_move.organization_id,
            part_number=prod.part_number,
            product_id=prod.id,
            location_id=loc_id
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=['location_id', 'product_id', 'date_key'],
            set_={
                'quantity': cls.quantity + 1
            }
        )
        session.execute(stmt)


class LocationPartNoTotals(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    __table_args__ = (db.UniqueConstraint("location_id", "product_id"),)
    organization_id = db.Column(db.Integer, index=True)
    location_id = db.Column(db.Integer, index=True)
    part_number = db.Column(db.String, index=True)
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, index=True)
    description = db.Column(db.Text(), default=None)

    @classmethod
    def get_by_location_id_and_prod_id(cls, loc_id, prod_id, session=None):
        stmt = select(cls).where(
            and_(
                cls.location_id == loc_id,
                cls.product_id == prod_id
            )
        )
        if session:
            return session.scalars(stmt).first()
        return db.session.scalars(stmt).first()

    @classmethod
    def upsert(cls, payload, session=None):
        loc_id = payload['loc_id']
        prod = payload['product']
        stmt = insert(cls).values(
            location_id=loc_id,
            description=prod.description,
            part_number=prod.part_number,
            product_id=prod.id,
            quantity=1,
            organization_id=prod.organization_id,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=['location_id', 'product_id'],
            set_={
                'quantity': cls.quantity + 1,
                'description': stmt.excluded.description
            }
        )
        session.execute(stmt)

    @classmethod
    def up_sert(cls, payload, session=None):
        loc_id = payload['loc_id']
        prod = payload['product']
        stmt = insert(cls).values(
            location_id=loc_id,
            description=prod.description,
            part_number=prod.part_number,
            product_id=prod.id,
            quantity=1,
            organization_id=prod.organization_id,
        ).on_conflict_do_nothing(
            index_elements=['location_id', 'product_id']
        )
        session.execute(stmt)

    @classmethod
    def upsert_src_loc_total(cls, payload, session=None):
        loc_id = payload['loc_id']
        prod = payload['product']
        count_subquery = select(func.count()).select_from(LicensePlate).where(
            LicensePlate.location_id == loc_id,
            LicensePlate.product_id == prod.id
        ).scalar_subquery()
        stmt = insert(cls).values(
            location_id=loc_id,
            description=prod.description,
            part_number=prod.part_number,
            product_id=prod.id,
            organization_id=prod.organization_id,
            quantity=count_subquery
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=['location_id', 'product_id'],
            set_={
                'quantity': cls.quantity - 1,
                'description': stmt.excluded.description 
            }
        )
        session.execute(stmt)
