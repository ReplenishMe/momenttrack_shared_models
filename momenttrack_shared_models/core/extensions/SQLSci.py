from active_alchemy import ActiveAlchemy
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import scoped_session
from sqlalchemy.engine.url import make_url

# conf = {
#     'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URL'),
#     'SQLALCHEMY_BINDS': {
#         "writer": WRITER_DB_URI,
#         "cache_refresher": DATABASE_URL_REFRESHER
#     }
# }


class SQLSci(ActiveAlchemy):
    uri: str

    def add_sessions(self, db_config, **kwargs):
        if 'SQLALCHEMY_BINDS' in db_config:
            for key, val in db_config['SQLALCHEMY_BINDS'].items():
                engine = create_engine(make_url(val), **kwargs)
                _factory = orm.sessionmaker(bind=engine)
                setattr(
                    self,
                    f'{key}_session',
                    scoped_session(_factory)
                )

    def __init__(self, db_config=None, **kwargs):
        if db_config:
            _uri = db_config['SQLALCHEMY_DATABASE_URI']
            self.uri = _uri
            ActiveAlchemy.__init__(self, uri=_uri, **kwargs)
            SQLSci.add_sessions(self, db_config)
        else:
            ActiveAlchemy.__init__(self, **kwargs)

    def init_db(self, db_config, **kwargs):
        _uri = db_config['SQLALCHEMY_DATABASE_URI']
        self.uri = _uri
        self.info = make_url(_uri)
        self.options['pool_size'] = kwargs.get('pool_size', None)
        self.options['pool_use_lifo'] = True
        self.options['pool_pre_ping'] = True
        self.add_sessions(db_config, **kwargs)
        self.session = self._create_scoped_session()
        # # new engine with passed pool size
        # self.engine.dispose()
        # self.engine = self.connector.get_engine()
        # print("new engine", self.engine.pool.size())
        return self
