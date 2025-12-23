import os
import enum
import random
import uuid


from flask import (
    jsonify, make_response
)
from opensearchpy import OpenSearch, RequestsHttpConnection


class DataValidationError(Exception):
    def __init__(self, message, errors, data=None):
        super(DataValidationError, self).__init__(message, errors, data)
        self.message = message
        self.errors = errors
        self.data = data

    def __reduce__(self):
        return (DataValidationError, (self.message, self.errors, self.data))


class SerializableEnum(str, enum.Enum):
    """JSON Serializable enums for easy response generation.
    Note: sub-classing str makes it serializable.
     see: https://stackoverflow.com/a/51976841/2528464
    """

    pass


def generate_token(length, special_chars=False, upper_case_only=True):
    chars = "abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ0123456789"

    if special_chars:
        chars += "~!@#$%^&*()?+_-[]{};><"

    token = "".join(random.choice(chars) for x in range(length))

    if upper_case_only:
        token = token.upper()

    return token


class AppResponse:
    SUCCESS = "success"
    PENDING = "pending"
    FAIL = "fail"
    ERROR = "error"

    @staticmethod
    def success(
        data=None, code=200, message=None,
        headers=None, status=None, pagination=None
    ):
        output = {
            "success": True,
            "data": data,
            "message": message,
            "errors": None,
            "status": status or AppResponse.SUCCESS,
            "pagination": pagination,
        }
        return make_response(jsonify(output), code, headers)

    @staticmethod
    def error(message, code, headers=None, errors=None):
        if type(message) is list:
            message = message[0]

        output = {
            "success": True,
            "data": None,
            "message": message,
            "errors": errors,
            "status": AppResponse.ERROR,
        }
        return make_response(jsonify(output), code, headers)


def generate_uuid():
    return uuid.uuid4().hex


def setup_opensearch():
    user = os.getenv('OPENSEARCH_USER')
    passphrase = os.getenv('OPENSEARCH_PASS')
    if not user or not passphrase:
        return
    auth_h = (
        os.getenv("OPENSEARCH_USER"),
        os.getenv("OPENSEARCH_PASS")
    )
    client = OpenSearch(
        hosts=[{"host": os.getenv("OPENSEARCH_HOST"), "port": 443}],
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        http_auth=auth_h,
        timeout=300,
    )
    return client
