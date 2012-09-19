======================
Source code for step 2 
======================


This is how models.py should look like at this point::

    import datetime
    from sqlalchemy import (
        Column,
        Integer,
        Text,
        Unicode,
        UnicodeText,
        DateTime
        )
    
    from webhelpers.text import urlify
    from webhelpers.paginate import PageURL
    from webhelpers.date import time_ago_in_words
    
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
        name = Column(Unicode, unique=True, nullable=False)
        password = Column(Unicode, nullable=False)
        last_logged = Column(DateTime, default=datetime.datetime.utcnow)
        
    class Entry(Base):
        __tablename__ = 'entries'
        id = Column(Integer, primary_key=True)
        title = Column(Unicode, unique=True, nullable=False)
        body = Column(UnicodeText, default=u'')
        created = Column(DateTime, default=datetime.datetime.utcnow)
        edited = Column(DateTime, default=datetime.datetime.utcnow)
              
This is how views.py should look like at this point::
        
    from pyramid.view import view_config
    
    from .models import (
        DBSession,
        User,
        )

This is how /scripts/initializedb.py should look like at this point::
        
    import os
    import sys
    import transaction
    
    from sqlalchemy import engine_from_config
    
    from pyramid.paster import (
        get_appsettings,
        setup_logging,
        )
    
    from ..models import (
        DBSession,
        User,
        Base,
        )
    
    def usage(argv):
        cmd = os.path.basename(argv[0])
        print('usage: %s <config_uri>\n'
              '(example: "%s development.ini")' % (cmd, cmd)) 
        sys.exit(1)
    
    def main(argv=sys.argv):
        if len(argv) != 2:
            usage(argv)
        config_uri = argv[1]
        setup_logging(config_uri)
        settings = get_appsettings(config_uri)
        engine = engine_from_config(settings, 'sqlalchemy.')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            admin = User(name=u'admin', password=u'admin')
            DBSession.add(admin)