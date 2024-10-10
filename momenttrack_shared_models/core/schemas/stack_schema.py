import marshmallow.fields as ma
from marshmallow import (
    post_load, pre_load,
    fields, ValidationError
)

from momenttrack_shared_models.core.database.models import (
    Stack, ProductionOrder,
    Product, Location
)
from momenttrack_shared_models.core.schemas._base import (
    BaseMASchema, BaseSQLAlchemyAutoSchema
)
from momenttrack_shared_models.core.extensions import db
from momenttrack_shared_models.core.schemas.utils import current_org
from momenttrack_shared_models.core.schemas.license_plate_schema import \
    LpMoveField

from momenttrack_shared_models.core.utils import DataValidationError


class StackSchema(BaseSQLAlchemyAutoSchema):
    class Meta:
        model = Stack
        load_instance = True
        include_relationships = True
        include_fk = True
    location_id = LpMoveField(required=True, allowed_len=11)

    @pre_load
    def preprocess_data(self, data, **kwargs):
        if data:
            if "product_id" not in data:
                product_id = None
                if "production_order_id" in data:
                    if isinstance(data["production_order_id"], str):
                        try:
                            product_id = (
                                ProductionOrder.query.filter_by(
                                    docid=data["production_order_id"]
                                )
                                .first()
                                .product_id
                            )
                        except Exception:
                            pass
                    if isinstance(data["production_order_id"], int):
                        try:
                            product_id = (
                                ProductionOrder.query.filter_by(
                                    id=data["production_order_id"]
                                )
                                .first()
                                .product_id
                            )
                        except Exception:
                            pass
                if product_id:
                    part_number = (
                                Product.query.filter_by(
                                    id=product_id
                                )
                                .first()
                                .part_number
                            )
                    data.update({"part_number": part_number})
                    data.update({"item_count": 0})

        return data

    @post_load
    def add_required_alt(self, data, *args, **kwargs):
        if data:

            if isinstance(data["location_id"], str):
                data["location_id"] = Location.query.filter(
                    Location.beacon_id == data["location_id"]
                ).first().id
        return data

    def validate(self, data):
        errors = {}
        for field_name, field_obj in self.fields.items():
            if field_obj.required:
                value = data.get(field_name)
                if value is None:
                    errors[field_name] = ["Field is required."]
        if errors:
            raise DataValidationError(errors)


class StringOrIntField(fields.Field):
    """Custom Marshmallow field that accepts either a string or an integer."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize the value to a string or an int."""
        if isinstance(value, (str, int)):
            return value
        raise ValidationError("Field should be either a string or an integer.")

    def _deserialize(self, value, attr, data, **kwargs):
        """Deserialize the value, accepting both string and integer."""
        if isinstance(value, (str, int)):
            return value
        raise ValidationError("Field should be either a string or an integer.")


class StackCheckSchema(BaseMASchema):
    license_plate_id = StringOrIntField(required=True)
    dest_location_id = StringOrIntField(required=True)
    user_id = StringOrIntField(required=False)

    @post_load
    def process(self, data, many=False, **kwargs):
        if isinstance(data["license_plate_id"], str):
            lps = Stack.get_lp_list_or_none(
                data["license_plate_id"],
                session=db.session
            )
            if lps:
                data["lps"] = lps
                return data
        else:
            return


class StackCloseSchema(BaseSQLAlchemyAutoSchema):
    stack_id = ma.String(required=True)  # read-only
    item_count = ma.Integer(required=True)
    user_id = ma.Integer(required=False)

    def validate(self, data):
        errors = {}
        for field_name, field_obj in self.fields.items():
            if field_obj.required:
                value = data.get(field_name)
                if value is None:
                    errors[field_name] = ["Field is required."]
        if errors:
            raise DataValidationError(errors)


class StackRespSchema(BaseSQLAlchemyAutoSchema):
    stack_id = ma.String(dump_only=True)  # read-only
    item_count = ma.Integer()
    status = ma.Method("get_status")

    def get_status(self, obj):
        return obj.status.name.lower() if obj.status else None


class StackLoggSchema(BaseMASchema):
    id = ma.Integer()
    stack_id = ma.String(dump_only=True)  # read-only
    part_number = ma.String(required=True)
    description = ma.Method("get_description")
    production_order_id = ma.String(required=True)
    # Assuming the status is represented as a string
    status = ma.String(required=False)
    item_count = ma.Integer()
    location_id = ma.Integer()
    user_id = ma.Integer(required=False)
    org_id = ma.Integer(required=False)
    created_at = ma.String(dump_only=True)

    def get_description(self, obj):
        prod_ord = ProductionOrder.get_by_docid_and_org(
            obj.production_order_id, current_org.id
        )

        prod = Product.get_by_id_and_org(prod_ord.product_id, current_org.id)
        return prod.description


class StackListRespSchema(BaseSQLAlchemyAutoSchema):
    stack_id = ma.String(dump_only=True)  # read-only
    item_count = ma.Integer()
    part_number = ma.String(required=True)
    status = ma.Method("get_status")
    description = ma.Method("get_description")
    created_at = ma.String(dump_only=True)

    def get_status(self, obj):
        return obj.status.name.lower() if obj.status else None

    def get_description(self, obj):
        prod_ord = ProductionOrder.get_by_docid_and_org(
            obj.production_order_id, current_org.id
        )

        prod = Product.get_by_id_and_org(prod_ord.product_id, current_org.id)
        return prod.description
