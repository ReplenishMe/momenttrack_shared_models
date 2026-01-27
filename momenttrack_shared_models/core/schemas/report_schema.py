import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import (
    BaseMASchema, BaseSQLAlchemyAutoSchema
)
from momenttrack_shared_models.core.database.models import (
    EverythingReport, LineItemTotals, LineGraphData,
    LocationPartNoTotals
)
from momenttrack_shared_models.core.extensions import db
from marshmallow import validate


class EverythingReportSchema(BaseSQLAlchemyAutoSchema):
    class Meta:
        model = EverythingReport
        sqla_session = db.session
        load_instance = True


class RequestReportSchema(BaseMASchema):
    email = ma.String(required=True, validate=validate.Email())


class LineItemTotalSchema(BaseSQLAlchemyAutoSchema):
    class Meta:
        model = LineItemTotals


class LineGraphDataSchema(BaseSQLAlchemyAutoSchema):
    class Meta:
        model = LineGraphData


class LocationPartNoTotalsSchema(BaseSQLAlchemyAutoSchema):
    class Meta:
        model = LocationPartNoTotals
