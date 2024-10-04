from . import settings
from .extensions import init_app

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    # init extensions
    init_app(app)
    return app
