from pyramid.view import view_config
from ..services.blog_record import BlogRecordService


@view_config(route_name='home',
             renderer='pyramid_blogr:templates/index.jinja2')
def index_page(request):
    page = int(request.params.get('page', 1))
    paginator = BlogRecordService.get_paginator(request, page)
    return {'paginator': paginator}


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    return {}
