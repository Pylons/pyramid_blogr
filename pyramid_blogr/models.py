import datetime
import sqlalchemy as sa
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    DateTime
    )

from webhelpers2.text import urlify
from webhelpers2.date import time_ago_in_words
from paginate import Page

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def by_name(cls, name):
        return DBSession.query(User).filter(User.name == name).first()
    
    def verify_password(self, password):
        return self.password == password

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    
    @classmethod
    def all(cls):
        return DBSession.query(Entry).order_by(sa.desc(Entry.created)).all()
    
    @classmethod
    def by_id(cls, id):
        return DBSession.query(Entry).filter(Entry.id == id).first()
    
    @property
    def slug(self):
        return urlify(self.title)
    
    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)
    
    @classmethod
    def get_paginator(cls, request, page=1):
        return Page(Entry.all(), page, items_per_page=5,
                    url_maker=lambda p: "%s?page=%s" % (request.application_url, p))
