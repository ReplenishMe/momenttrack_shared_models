import os

from dotenv import load_dotenv

from momenttrack_shared_models import LicensePlate, Activity, ActivityTypeEnum, Container
from momenttrack_shared_models.core.extensions import db
from momenttrack_shared_models.core.schemas import LicensePlateSchema



load_dotenv()


WRITER_DB_URI = os.getenv("DATABASE_URL_WRITER", "sqlite:///dev.db")
DATABASE_URL_REFRESHER = os.getenv("DATABASE_URL_REFRESHER", "sqlite:///dev.db")
conf = {
    'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URL'),
    'SQLALCHEMY_BINDS': {
        "writer": WRITER_DB_URI,
        "cache_refresher": DATABASE_URL_REFRESHER
    }
}
schema = LicensePlateSchema(unknown='exclude')
obj = {'production_order_id': 1034, 'quantity': 1, 'product_id': 1, 'lp_id': 'qf6a5wwdoefwadd1c149d1009'}


# print(dir(db.init_db(conf)))
db.init_db(conf, pool_size=20)
# from pprint import pprint as pp
# pp(vars(LicensePlate))
print(schema.load(obj, session=db.writer_session()))
# activity = Activity(
#     model_name="license_plate",
#     model_id=5918,
#     user_id=3,
#     loggedin_user_id=3,
#     organization_id=4,
#     message="message",
#     activity_type=ActivityTypeEnum.LICENSE_PLATE_MOVE,
#     ip_address="127..0.0.1",
# )
# print(vars(activity))
# db.writer_session.add(activity)
# db.writer_session.commit()
# print(vars(Activity.get(activity.id)))
# db.writer_session.rollback()
# db.writer_session.close()
# schema = LicensePlateSchema()
# lp = LicensePlate.get(1)
# print(schema.dump(lp))
# print(LicensePlate.get(1).lp_id)
# print(dir(LicensePlate.get(1)))
# print(len(LicensePlate.query.filter_by(organization_id=4).all()))
