import datetime #<- will be used to set default dates on models
import sqlalchemy as sa #<- provides access to sqlalchemy constructs
from pyramid_blogr.models import Base, DBSession #<- we need to import our sqlalchemy metadata for model classes to inherit from
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,     #<- will provide unicode field,
    UnicodeText, #<- will provide unicode text field,
    DateTime     #<- time abstraction field,
)

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