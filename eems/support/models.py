from sqlalchemy import Column, Integer, Text
from database import Base


class General(Base):
    __tablename__ = 'GENERAL'
    id = Column('ID', Integer, primary_key=True, unique=True)
    item = Column('ITEM', Text)
    value = Column('VALUE', Text)

    def __init__(self, id=None, item=None, value=None):
        self.id = id
        self.item = item
        self.value = value


class Content(Base):
    __tablename__ = 'CONTENT'
    id = Column('ID', Integer, primary_key=True, unique=True)
    position = Column('POSITION', Text)
    german = Column('GERMAN', Text)
    english = Column('ENGLISH', Text)

    def __init__(self, id=None, position=None, german=None, english=None):
        self.id = id
        self.position = position
        self.german = german
        self.english = english


class Sessions(Base):
    __tablename__ = 'SESSIONS'
    id = Column('ID', Integer, primary_key=True, unique=True)
    session = Column('SESSION', Text, unique=True)
    frontend = Column('FRONTEND', Text)
    backend = Column('BACKEND', Text)

    def __init__(self, id=None, session=None, frontend=None, backend=None):
        self.id = id
        self.session = session
        self.frontend = frontend
        self.backend = backend


class Test(Base):
    __tablename__ = 'TEST'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', Text)
