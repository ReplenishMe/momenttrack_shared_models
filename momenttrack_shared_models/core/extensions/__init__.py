from passlib.context import CryptContext

from .SQLSci import SQLSci
from dotenv import load_dotenv
from momenttrack_shared_models.core.utils import setup_opensearch

from ..database.base_query import AppBaseQuery

from flask_migrate import Migrate

load_dotenv()


db = SQLSci(query_cls=AppBaseQuery)
pwd_context = CryptContext(schemes=["pbkdf2_sha512"], deprecated="auto")
migrate = Migrate(db)
open_client = setup_opensearch()


def init_app(app):
    migrate.init_app(app, db)
