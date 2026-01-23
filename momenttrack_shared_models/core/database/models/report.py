from dataclasses import dataclass

from sqlalchemy import select, and_

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
        lp_id = payload['lp_id']
        po_id = payload['po_id']
        report_raw = payload['report_raw']
        existing_row = cls.get_by_license_plate_id(
            lp_id, session=session
        )
        resp = EverythingReportResp()
        if existing_row:
            for k, v in report_raw.items():
                setattr(existing_row, k, v)
        else:
            new_stat = cls(**report_raw)
            resp.is_new = True
            resp.new_object = new_stat
        return resp


@dataclass
class EverythingReportResp:
    new_object: EverythingReport = None
    is_new: bool = False


class LineItemTotals(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
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
        existing_row = cls.get_by_location_and_order(
            location.id, po_id, session=session
        )
        resp = LineItemTotalsResp()
        if existing_row:
            existing_row.total_items += 1
            resp.totals_object = existing_row
        else:
            new_stat = cls(
                name=location.name,
                production_order_id=po_id,
                location_id=location.id,
                organization_id=location.organization_id,
                total_items=1
            )
            resp.is_new = True
            resp.totals_object = new_stat
        return resp


@dataclass
class LineItemTotalsResp:
    totals_object: LineItemTotals = None
    is_new: bool = False


class LineGraphData(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    organization_id = db.Column(db.Integer, index=True)
    date = db.Column(db.DateTime)
    date_key = db.Column(db.String, index=True)
    location_id = db.Column(db.Integer)
    part_number = db.Column(db.String)
