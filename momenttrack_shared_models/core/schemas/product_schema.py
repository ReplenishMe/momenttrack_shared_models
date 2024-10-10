import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.database.models import LicensePlate, Product
from momenttrack_shared_models.core.extensions import db


class ProductSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only
    preferred_vendor = ma.Nested("VendorSchema", dump_only=True)  # read-only

    class Meta:
        exclude = ("updated_at",)
        model = Product
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class ProductDumpSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only
    preferred_vendor = ma.Nested("VendorSchema", dump_only=True)  # read-only

    class Meta:
        exclude = ("updated_at",)
        model = Product
        sqla_session = db.session
        include_fk = True


class ProductReportLicensePlateSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only

    class Meta:
        exclude = ("updated_at", "organization_id")
        model = LicensePlate
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class ProductReportSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only
    license_plates = ma.Nested(
        ProductReportLicensePlateSchema, dump_only=True, many=True
    )  # read-only

    class Meta:
        exclude = ("updated_at", "license_plate_move")
        model = Product
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True
