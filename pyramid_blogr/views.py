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
    id = int(request.matchdict.get('entry_id', -1))
    entry = Entry.by_id(id)
    if not entry:
        return HTTPNotFound()
    return {'entry':entry}

@view_config(route_name='blog_action', match_param="action=create",
             renderer="pyramid_blogr:templates/edit_blog.mako")
@view_config(route_name='blog_action', match_param="action=edit",
             renderer="pyramid_blogr:templates/edit_blog.mako")
def blog_create_update(request):
    return {}

@view_config(route_name='sign_in', renderer="string", request_method="POST")
def sign_in(request):
    return {}

@view_config(route_name='sign_out', renderer="string")
def sign_out(request):
    return {}
