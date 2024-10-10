import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseMASchema


class NewOrgSchema(BaseMASchema):
    name = ma.String(required=True)
    email = ma.Email(required=True)
    password = ma.String(required=True)
    org_name = ma.String(required=True)
    org_slug = ma.String(required=False)
    org_address = ma.String(required=False)
