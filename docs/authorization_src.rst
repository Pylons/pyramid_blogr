======================
Source code for step 7
======================

This is how __init__.py should look like at this point::

    from pyramid.config import Configurator
    from sqlalchemy import engine_from_config
    from pyramid.authentication import AuthTktAuthenticationPolicy
    from pyramid.authorization import ACLAuthorizationPolicy
    from .security import EntryFactory

    from .models import (
        DBSession,
        Base,
        )


    def main(global_config, **settings):
        """ This function returns a Pyramid WSGI application.
        """
        engine = engine_from_config(settings, 'sqlalchemy.')
        DBSession.configure(bind=engine)
        Base.metadata.bind = engine
        authentication_policy = AuthTktAuthenticationPolicy('somesecret', hashalg='sha512')
        authorization_policy = ACLAuthorizationPolicy()
        config = Configurator(settings=settings,
                              authentication_policy=authentication_policy,
                              authorization_policy=authorization_policy
        )
        config.include('pyramid_mako')
        config.add_static_view('static', 'static', cache_max_age=3600)
        config.add_route('home', '/')
        config.add_route('blog', '/blog/{id:\d+}/{slug}')
        config.add_route('blog_action', '/blog/{action}',
                         factory='pyramid_blogr.security.EntryFactory')
        config.add_route('auth', '/sign/{action}')
        config.scan()
        return config.make_wsgi_app()



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
