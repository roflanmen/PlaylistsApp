from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.orm import sessionmaker, Session
from app.models import *
from app import app
import config

def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

engine = create_engine(app.config['SQLALCHEMY_DATABASE_STR'], echo=False, connect_args={'check_same_thread': False})
event.listen(engine, 'connect', _fk_pragma_on_connect)

metadata = Base.metadata
Session = sessionmaker(bind=engine)
session = Session()

if config.is_testing:
    metadata.drop_all(engine)
try:
    metadata.create_all(engine)
except:
    pass
