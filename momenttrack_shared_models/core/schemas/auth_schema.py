import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseMASchema
from momenttrack_shared_models.core.schemas._validators import \
     validate_password


class LoginSchema(BaseMASchema):
    email = ma.Email(required=True)
    password = ma.String(required=True)


class LoginResponseSchema(BaseMASchema):
    access_token = ma.String()


# class InviteUserSchema(BaseMASchema):
#     email = ma.Email(required=True)


class AcceptInviteSchema(BaseMASchema):
    token = ma.String(required=True)


class RequestPasswordResetSchema(BaseMASchema):
    email = ma.Email(required=True)


class ChangePasswordSchema(BaseMASchema):
    password = ma.String(required=True, validate=[validate_password])
