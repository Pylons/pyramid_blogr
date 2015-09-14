======================
Source code for step 6 
======================

Contents of forms.py::

    from wtforms import Form, StringField, TextAreaField, validators
    from wtforms import HiddenField

    strip_filter = lambda x: x.strip() if x else None

    class BlogCreateForm(Form):
        title = StringField('Title', [validators.Length(min=1, max=255)],
                            filters=[strip_filter])
        body = TextAreaField('Contents', [validators.Length(min=1)],
                             filters=[strip_filter])

    class BlogUpdateForm(BlogCreateForm):
        id = HiddenField()

Contents of views/blog.py::

    from pyramid.view import view_config
    from pyramid.httpexceptions import HTTPNotFound, HTTPFound
    from ..models.meta import DBSession
    from ..models.blog_record import BlogRecord
    from ..models.services.blog_record import BlogRecordService
    from ..forms import BlogCreateForm, BlogUpdateForm

    @view_config(route_name='blog', renderer='pyramid_blogr:templates/view_blog.mako')
    def blog_view(request):
        blog_id = int(request.matchdict.get('id', -1))
        entry = BlogRecordService.by_id(blog_id)
        if not entry:
            return HTTPNotFound()
        return {'entry': entry}

    @view_config(route_name='blog_action', match_param='action=create',
                 renderer='pyramid_blogr:templates/edit_blog.mako')
    def blog_create(request):
        entry = BlogRecord()
        form = BlogCreateForm(request.POST)
        if request.method == 'POST' and form.validate():
            form.populate_obj(entry)
            DBSession.add(entry)
            return HTTPFound(location=request.route_url('home'))
        return {'form': form, 'action': request.matchdict.get('action')}

    @view_config(route_name='blog_action', match_param='action=edit',
                 renderer='pyramid_blogr:templates/edit_blog.mako')
    def blog_update(request):
        blog_id = int(request.params.get('id', -1))
        entry = BlogRecordService.by_id(blog_id)
        if not entry:
            return HTTPNotFound()
        form = BlogUpdateForm(request.POST, entry)
        if request.method == 'POST' and form.validate():
            form.populate_obj(entry)
            return HTTPFound(location=request.route_url('blog', id=entry.id,
                                                        slug=entry.slug))
        return {'form': form, 'action': request.matchdict.get('action')}

