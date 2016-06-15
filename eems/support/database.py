# -*- coding: utf-8 -*-
"""
database module providing SQLAlchemy
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# check if server or development environment
if os.path.exists('/var/www/eems/eems/data/db/'):
    path = '/var/www/eems/eems/data/db/config.db'
else:
    path = '{}/data/db/config.db'.format(os.path.dirname(os.path.dirname(__file__)))

engine = create_engine('sqlite:////{}'.format(path), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)


