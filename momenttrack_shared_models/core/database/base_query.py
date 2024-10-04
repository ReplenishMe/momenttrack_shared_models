from flask import request
from flask_sqlalchemy import query
from sqlalchemy_filters import apply_filters


class AppBaseQuery(query.Query):
    """Custom sqlalchemy base query that extends Flask-SQLAlchemy base query

    https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery
    """

    def pagination(self):
        """Customize default paginate function from Flask-sqlalchemy"""
        page = self.paginate(page=None, per_page=20, error_out=False, max_per_page=100)

        return {
            "items": page.items,
            "page": page.page,
            "has_next": page.has_next,
            "count": page.per_page,
            "total_count": page.total,
        }

    def get_column_names(self):
        """Get list of columns names from table"""
        col_list = []
        for coldesc in self.column_descriptions:
            model = coldesc["entity"]
            col_list += [str(col).split(".")[-1] for col in model.__table__.columns]

        return col_list

    def apply_filters(self):
        """Generates query filters based on GET query params

        Ignore params that are not present in col names
        """
        query_params = request.args

        valid_fields = self.get_column_names()
        # For now, equality only.
        filter_spec = []
        for field, value in query_params.items():
            if field in valid_fields:
                filter_spec.append({"field": field, "op": "==", "value": value})

        filtered_query = apply_filters(self, filter_spec)

        return filtered_query
