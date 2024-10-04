import datetime
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load dotenv
ENV = os.getenv("ENV", "-unk-")

load_dotenv(verbose=True)

print("DB Connection", os.getenv('DATABASE_URL'))


DB_PASS = os.getenv("DB_PASS_LOCAL")
SQLALCHEMY_DATABASE_URI = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://localhost:5432"
    ),
)
WRITER_DB_URI = os.getenv("DATABASE_URL_WRITER", "sqlite:///dev.db")
DATABASE_URL_REFRESHER = os.getenv("DATABASE_URL_REFRESHER", "sqlite:///dev.db")
SQLALCHEMY_BINDS = {
    "writer": WRITER_DB_URI,
    "cache_refresher": DATABASE_URL_REFRESHER
}
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_RECORD_QUERIES = False  # good for debugging


pre_emptive_log_level = (
    "DEBUG"
    if (ENV == "-unk-" or ENV.lower() in ["dev", "develop", "devlopment"])
    else "WARNING"
)
LOG_LEVEL = os.getenv("LOG_LEVEL") if os.getenv("LOG_LEVEL") \
    else pre_emptive_log_level
LOG_DIR = os.getenv("LOG_DIR", "/tmp")
LOG_NAME = os.getenv("LOG_NAME", "ordertrack_api.log")
