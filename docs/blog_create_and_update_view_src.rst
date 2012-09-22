======================
Source code for step 6 
======================

Contents of forms.py::

    from wtforms import Form, BooleanField, TextField, TextAreaField, validators
    from wtforms import HiddenField
    
    strip_filter = lambda x: x.strip() if x else None
    
    class BlogCreateForm(Form):
        title = TextField('Entry title', [validators.Length(min=1, max=255)],
                          filters=[strip_filter])
        body = TextAreaField('Entry body', [validators.Length(min=1)],
                             filters=[strip_filter])
        
    class BlogUpdateForm(BlogCreateForm):
        id = HiddenField()

Contents of views.py::

    from .forms import BlogCreateForm, BlogUpdateForm
    from pyramid.httpexceptions import HTTPNotFound, HTTPFound
    from pyramid.response import Response
    from pyramid.view import view_config
    
    from sqlalchemy.exc import DBAPIError
    
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
        entry = Entry()
        form = BlogCreateForm(request.POST)
        if request.method == 'POST' and form.validate():
            form.populate_obj(entry)
            DBSession.add(entry)
            return HTTPFound(location=request.route_url('home'))
        return {'form':form, 'action':request.matchdict.get('action')}
    
    
    @view_config(route_name='blog_action', match_param="action=edit",
                 renderer="pyramid_blogr:templates/edit_blog.mako")
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
    
    
    @view_config(route_name='auth', match_param="action=in", renderer="string",
                 request_method="POST")
    @view_config(route_name='auth', match_param="action=out", renderer="string")
    def sign_in_out(request):
        return {}
