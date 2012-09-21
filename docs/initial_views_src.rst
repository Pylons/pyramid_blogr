======================
Source code for step 4
======================

Contents of views.py::

    from pyramid.view import view_config
    
    from .models import (
        DBSession,
        User,
        )
    
    @view_config(route_name='home', renderer="pyramid_blogr:templates/index.mako")
    def index_page(request):
        return {}
    
    @view_config(route_name='blog', renderer="pyramid_blogr:templates/view_blog.mako")
    def blog_view(request):
        return {}
    
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

