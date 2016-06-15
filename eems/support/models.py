from sqlalchemy import Column, Integer, Text
from database import Base


class General(Base):
    __tablename__ = 'GENERAL'
    id = Column('ID', Integer, primary_key=True, unique=True)
    item = Column('ITEM', Text)
    value = Column('VALUE', Text)

    def __init__(self, item=None, value=None):
        self.item = item
        self.value = value


class Content(Base):
    __tablename__ = 'CONTENT'
    id = Column('ID', Integer, primary_key=True, unique=True)
    position = Column('POSITION', Text)
    german = Column('GERMAN', Text)
    english = Column('ENGLISH', Text)
