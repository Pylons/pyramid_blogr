======================
Source code for step 8
======================

This is how views/default.py should look like at this point::

    from pyramid.view import view_config
    from pyramid.httpexceptions import HTTPFound
    from pyramid.security import remember, forget

    from ..models import DBSession
    from ..models.user import User
    from ..models.entry import Entry

    @view_config(route_name='home', renderer='pyramid_blogr:templates/index.mako')
    def index_page(request):
        page = int(request.params.get('page', 1))
        paginator = Entry.get_paginator(request, page)
        return {'paginator': paginator}

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


This is how views/blog.py should look like at this point::

    from pyramid.view import view_config
    from pyramid.httpexceptions import HTTPNotFound, HTTPFound
    from ..models import DBSession
    from ..models.entry import Entry
    from ..forms import BlogCreateForm, BlogUpdateForm

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

        @classmethod
        def by_name(cls, name):
            return DBSession.query(User).filter(User.name == name).first()

        def verify_password(self, password):
            return self.password == password

This is how /templates/index.mako should look like at this point::
        
    <%inherit file="pyramid_blogr:templates/layout.mako"/>
    <% link_attr={"class": "btn btn-default btn-xs"} %>
    <% curpage_attr={"class": "btn btn-default btn-xs disabled"} %>
    <% dotdot_attr={"class": "btn btn-default btn-xs disabled"} %>

    % if request.authenticated_userid:
        Welcome <strong>${request.authenticated_userid}</strong> ::
        <a href="${request.route_url('auth',action='out')}">Sign Out</a>
    %else:
        <form action="${request.route_url('auth',action='in')}" method="post" class="form-inline">
            <div class="form-group">
                <label>User</label> <input type="text" name="username" class="form-control">
            </div>
            <div class="form-group">
            <label>Password</label> <input type="password" name="password" class="form-control">
            <input type="submit" value="Sign in" class="btn btn-default">
            </div>
        </form>
    %endif

    % if paginator.items:

        <h2>Blog entries</h2>

        <ul>
            % for entry in paginator.items:
                <li>
                    <a href="${request.route_url('blog', id=entry.id, slug=entry.slug)}">
                        ${entry.title}</a>
                </li>
            % endfor
        </ul>

        ${paginator.pager(link_attr=link_attr, curpage_attr=curpage_attr, dotdot_attr=dotdot_attr) |n}

    % else:

        <p>No blog entries found.</p>

    %endif

    <p><a href="${request.route_url('blog_action',action='create')}">
        Create a new blog entry</a></p>
