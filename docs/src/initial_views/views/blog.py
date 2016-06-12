from pyramid.view import view_config


@view_config(route_name='blog',
             renderer='pyramid_blogr:templates/view_blog.jinja2')
def blog_view(request):
    return {}


@view_config(route_name='blog_action', match_param='action=create',
             renderer='pyramid_blogr:templates/edit_blog.jinja2')
def blog_create(request):
    return {}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='pyramid_blogr:templates/edit_blog.jinja2')
def blog_update(request):
    return {}
