======================
Source code for step 2 
======================


This is how models/__init__.py should look like at this point::

    from sqlalchemy.ext.declarative import declarative_base

    from sqlalchemy.orm import (
        scoped_session,
        sessionmaker,
    )

    from zope.sqlalchemy import ZopeTransactionExtension

    DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    Base = declarative_base()

    from .user import User
    from .entry import Entry

              
This is how models/entry.py should look like at this point::
        
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

    class Entry(Base):
        __tablename__ = 'entries'
        id = Column(Integer, primary_key=True)
        title = Column(Unicode(255), unique=True, nullable=False)
        body = Column(UnicodeText, default=u'')
        created = Column(DateTime, default=datetime.datetime.utcnow)
        edited = Column(DateTime, default=datetime.datetime.utcnow)

This is how models/user.py should look like at this point::

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

This is how /scripts/initializedb.py should look like at this point::
        
    import os
    import sys
    import transaction

    from sqlalchemy import engine_from_config

    from pyramid.paster import (
        get_appsettings,
        setup_logging,
        )

    from pyramid.scripts.common import parse_vars

    from ..models import (
        DBSession,
        Base,
        User
        )


    def usage(argv):
        cmd = os.path.basename(argv[0])
        print('usage: %s <config_uri> [var=value]\n'
              '(example: "%s development.ini")' % (cmd, cmd))
        sys.exit(1)


    def main(argv=sys.argv):
        if len(argv) < 2:
            usage(argv)
        config_uri = argv[1]
        options = parse_vars(argv[2:])
        setup_logging(config_uri)
        settings = get_appsettings(config_uri, options=options)
        engine = engine_from_config(settings, 'sqlalchemy.')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            admin = User(name=u'admin', password=u'admin')
            DBSession.add(admin)
