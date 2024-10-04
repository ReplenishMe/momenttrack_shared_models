import re

from ..extensions import db
from ..utils.exceptions import DataValidationError
from sqlalchemy.exc import IntegrityError

# Ref: https://github.com/openstack/oslo.db/blob/0265aa4e01/oslo/db/sqlalchemy/exc_filters.py


def validate_unique_violation(e):
    """checks if db error is related to unique violation & if yes, returns the column name"""

    if not isinstance(e, IntegrityError):
        return None

    def _parse_duplicate_col(e):
        dup_key_regexes = [
            re.compile(
                r'^.*duplicate\s+key.*"(?P<columns>[^"]+)"\s*\n.*'
                r"Key\s+\((?P<key>.*)\)=\((?P<value>.*)\)\s+already\s+exists.*$"
            ),
            re.compile(r"^.*duplicate\s+key.*\"(?P<columns>[^\"]+)\"\s*\n.*$"),
        ]

        for dup_key_regex in dup_key_regexes:
            parsed = dup_key_regex.findall(e._message())
            parsed = parsed[0]

            if type(parsed) == tuple:
                fk = parsed[0]
                cols = [col.strip() for col in parsed[1].split(",")]
                vals = [col.strip() for col in parsed[2].split(",")]
                break

        # remove org_id col if exists
        if "organization_id" in cols:
            cols.remove("organization_id")

        return cols

    ### Check if unique key violation ###
    PG_UNIQUE_VIOLATION_CONSTANT = 23505
    try:
        if int(e.orig.pgcode) == PG_UNIQUE_VIOLATION_CONSTANT:
            return _parse_duplicate_col(e)
    except Exception as e:
        # brute force check
        if "duplicate key value violates unique constraint" in e.args[0]:
            return _parse_duplicate_col(e)


def validate_foreignkey_violation(e):
    ### Check if foreign key violation ###

    if not isinstance(e, IntegrityError):
        return None

    def _parse_foreign_key_error(e):
        """Parse foreign key error"""
        msg = e._message()
        foreign_key_regex = re.compile(
            r".*DETAIL:  Key \((?P<key>.+)\)=\(.+\) is not present in table \"(?P<key_table>[^\"]+)\""
        )

        try:
            col, table = foreign_key_regex.findall(msg)[0]
            return f"Provided {col} does not exist"
        except Exception as e:
            return None

    PG_FOREIGN_KEY_VIOLATION = 23503
    try:
        if int(e.orig.pgcode) == PG_FOREIGN_KEY_VIOLATION:
            return _parse_foreign_key_error(e)
    except Exception as e:
        return "Invalid value for one of the columns"

    return None


def DBErrorHandler(e):
    """handle certain db related exceptions"""
    db.session.rollback()
    db.writer_session.rollback()

    # 1. Check if error is due to unique constraint violation
    uniq_error_cols = validate_unique_violation(e)
    if uniq_error_cols:
        errors = {}
        for col in uniq_error_cols:
            errors[col] = [f"{col} already exists"]

        raise DataValidationError(
            message="One or more fields already exist in the database", errors=errors
        )

    # 2. Check if foreign key violation
    foreign_key_error = validate_foreignkey_violation(e)
    if foreign_key_error is not None:
        raise DataValidationError(message=foreign_key_error, errors=None)

    # 3. check if data related error

    # if not these, just raise back as is
    raise e
