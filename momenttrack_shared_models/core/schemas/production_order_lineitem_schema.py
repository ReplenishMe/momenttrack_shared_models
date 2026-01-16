import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.database.models import ProductionOrderLineitem
from momenttrack_shared_models.core.extensions import db


class ProductionOrderLineitemSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only

    class Meta:
        exclude = ("updated_at",)
        model = ProductionOrderLineitem
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class ProductionOrderLineitemOrderReportSchema(BaseSQLAlchemyAutoSchema):
    class Meta:
        include_relationships = True
        fields = (
            'license_plate', 'production_order'
        )

    license_plate = ma.Nested('LicensePlateOrderReportSchema')
    production_order = ma.Nested(
        'ProductionOrderSchema', only=(
            'product.description',
            'product.part_number',
        )
    )
