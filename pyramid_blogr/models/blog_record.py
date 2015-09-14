import datetime #<- will be used to set default dates on models
from pyramid_blogr.models.meta import Base  #<- we need to import our sqlalchemy metadata for model classes to inherit from
from sqlalchemy import (
    Column,
    Integer,
    Unicode,     #<- will provide unicode field,
    UnicodeText, #<- will provide unicode text field,
    DateTime     #<- time abstraction field,
)
from webhelpers2.text import urlify #<- will generate slugs
from webhelpers2.date import time_ago_in_words #<- human friendly dates

class BlogRecord(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)
