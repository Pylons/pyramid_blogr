======================
Source code for step 5
======================

Contents of models.py::

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
    
    from webhelpers.text import urlify
    from webhelpers.paginate import PageURL_WebOb, Page
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
        name = Column(Unicode(255), unique=True, nullable=False)
        password = Column(Unicode(255), nullable=False)
        last_logged = Column(DateTime, default=datetime.datetime.utcnow)
        
    class Entry(Base):
        __tablename__ = 'entries'
        id = Column(Integer, primary_key=True)
        title = Column(Unicode(255), unique=True, nullable=False)
        body = Column(UnicodeText, default=u'')
        created = Column(DateTime, default=datetime.datetime.utcnow)
        edited = Column(DateTime, default=datetime.datetime.utcnow)
        
        @classmethod
        def all(cls):
            return DBSession.query(Entry).order_by(sa.desc(Entry.created))
    
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
            page_url = PageURL_WebOb(request)
            return Page(Entry.all(), page, url=page_url, items_per_page=5)
        

Contents of views.py::
        
    from pyramid.view import view_config
    
    from pyramid.httpexceptions import HTTPNotFound, HTTPFound
    
    from .models import (
        DBSession,
        User,
        Entry
        )
    
    @view_config(route_name='home', renderer="pyramid_blogr:templates/index.mako")
    def index_page(request):
        page = int(request.params.get('page', 1))
        paginator = Entry.get_paginator(request, page)
        return {'paginator':paginator}
    
    @view_config(route_name='blog', renderer="pyramid_blogr:templates/view_blog.mako")
    def blog_view(request):
        id = int(request.matchdict.get('id', -1))
        entry = Entry.by_id(id)
        if not entry:
            return HTTPNotFound()
        return {'entry':entry}
    
    @view_config(route_name='blog_action', match_param="action=create",
                 renderer="pyramid_blogr:templates/edit_blog.mako")
    def blog_create(request):
        return {}
        
    @view_config(route_name='blog_action', match_param="action=edit",
                 renderer="pyramid_blogr:templates/edit_blog.mako")
    def blog_update(request):
        return {}
    
    @view_config(route_name='sign', match_param="action=in", renderer="string",
                 request_method="POST")
    @view_config(route_name='sign', match_param="action=out", renderer="string")
    def sign_in_out(request):
        return {}
