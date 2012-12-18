======================
Source code for step 8
======================

This is how views.py should look like at this point::

    from .forms import BlogCreateForm, BlogUpdateForm
    from pyramid.httpexceptions import HTTPNotFound, HTTPFound
    from pyramid.response import Response
    from pyramid.security import remember, forget
    from pyramid.view import view_config
    
    from sqlalchemy.exc import DBAPIError
    
    from .models import (
        DBSession,
        User,
        Entry
        )
    
    @view_config(route_name='home', renderer='pyramid_blogr:templates/index.mako')
    def index_page(request):
        page = int(request.params.get('page', 1))
        paginator = Entry.get_paginator(request, page)
        return {'paginator':paginator}
    
    
    @view_config(route_name='blog', renderer='pyramid_blogr:templates/view_blog.mako')
    def blog_view(request):
        id = int(request.matchdict.get('id', -1))
        entry = Entry.by_id(id)
        if not entry:
            return HTTPNotFound()
        return {'entry':entry}
    
    
    @view_config(route_name='blog_action', match_param='action=create',
                 renderer='pyramid_blogr:templates/edit_blog.mako',
                 permission='create')
    def blog_create(request):
        entry = Entry()
        form = BlogCreateForm(request.POST)
        if request.method == 'POST' and form.validate():
            form.populate_obj(entry)
            DBSession.add(entry)
            return HTTPFound(location=request.route_url('home'))
        return {'form':form, 'action':request.matchdict.get('action')}
    
    
    @view_config(route_name='blog_action', match_param='action=edit',
                 renderer='pyramid_blogr:templates/edit_blog.mako',
                 permission='edit')
    def blog_update(request):
        id = int(request.params.get('id', -1))
        entry = Entry.by_id(id)
        if not entry:
            return HTTPNotFound()
        form = BlogUpdateForm(request.POST, entry)
        if request.method == 'POST' and form.validate():
            form.populate_obj(entry)
            return HTTPFound(location=request.route_url('blog', id=entry.id,
                                                        slug=entry.slug))
        return {'form':form, 'action':request.matchdict.get('action')}
    
    
    @view_config(route_name='auth', match_param='action=in', renderer='string',
                 request_method='POST')
    @view_config(route_name='auth', match_param='action=out', renderer='string')
    def sign_in_out(request):
        username = request.POST.get('username')
        if username:
            user = User.by_name(username)
            if user and user.verify_password(request.POST.get('password')):
                headers = remember(request, user.name)
            else:
                headers = forget(request)
        else:
            headers = forget(request)
        return HTTPFound(location=request.route_url('home'),
                         headers=headers)

                     
This is how models.py should look like at this point::
    
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

This is how /templates/index.mako should look like at this point::
        
    <%inherit file="pyramid_blogr:templates/layout.mako"/>
    <%
    from pyramid.security import authenticated_userid 
    user_id = authenticated_userid(request)
    %>
    % if user_id:
        Welcome <strong>${user_id}</strong> :: 
        <a href="${request.route_url('auth',action='out')}">Sign Out</a>
    %else:
        <form action="${request.route_url('auth',action='in')}" method="post">
        <label>User</label><input type="text" name="username">
        <label>Password</label><input type="password" name="password">
        <input type="submit" value="Sign in">
        </form>
    %endif
    
    % if paginator.items:
    
        ${paginator.pager()}
    
        <h2>Blog entries</h2>
    
        <ul>
        % for entry in paginator.items:
        <li>
        <a href="${request.route_url('blog', id=entry.id, slug=entry.slug)}">
        ${entry.title}</a>
        </li>
        % endfor
        </ul>
    
        ${paginator.pager()}
    
    % else:
    
    <p>No blog entries found.</p>
    
    %endif
    
    <p><a href="${request.route_url('blog_action',action='create')}">
    Create a new blog entry</a></p>
