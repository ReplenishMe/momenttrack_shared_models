from ..model_mixins import BelongsToOrgMixin, IdMixin
from ...extensions import db


class EverythingReport(db.Model, IdMixin, BelongsToOrgMixin):
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
