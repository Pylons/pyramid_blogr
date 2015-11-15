================
4. Initial views
================

Now it's time to create our views files and add our view callables.

Every view will be decorated with **@view_config** decorator.

**@view_config** will configure our pyramid application by telling it how to 
corellate our view callables with routes, also setting some restrictions on 
specific view resolution mechanisms.
It's is being picked up when config.scan() gets run from our __init__.py, 
all of our views are registerd with our app.

.. note::
    You could do it explictly with **config.add_view()** method 
    but this approach is often more convenient. 

First lets create a new package called views and create 3 files, `views/__init__.py`,
`views/default.py` and `views/blog.py`.

Your project structure should look like this at this point::

    pyramid_blogr/
    ├── __init__.py <- main file that will configure and return WSGI application
    ├── models      <- model definitions aka data sources (often RDBMS or noSQL)
    │     ├── __init__.py
    │     ├── meta.py <- former models.py
    │     ├── blog_record.py
    │     └── user.py
    ├── scripts/    <- util python scripts
    ├── static/     <- usually css, js, images
    ├── templates/  <- template files
    ├── tests.py    <- tests
    └── views    <- views aka business logic
          ├── __init__.py <- empty
          ├── blog.py
          └── default.py

Lets make some stubs for our views, we will populate them with actual
code in next chapters.

In `views/default.py` add::

    from pyramid.view import view_config

    @view_config(route_name='home', renderer='pyramid_blogr:templates/index.jinja2')
    def index_page(request):
        return {}
    
Here @view_config takes 2 params that will register our index_page callable 
within pyramid's registry, specifying the route that should be used to match this 
view, we also specified renderer that will be used to transform the data view 
returns into response suitable for the client.

The template location is specified using *asset location* format which is in 
form of *package_name:path_to_template*.

.. note::
    It also easy to add your own custom renderer, or use a drop in package like 
    `pyramid_jinja2`.
    
    The renderer is picked up automaticly by specifying file extension 
    like: *asset.jinja2*/*asset.jinja2* or when your provide name for
    string/json renderer.   
    
    Pyramid by provides few renderers including:
        * mako templates
        * chameleon templates
        * string output
        * json encoder


In `views/blog.py` add::

    from pyramid.view import view_config

    @view_config(route_name='blog', renderer='pyramid_blogr:templates/view_blog.jinja2')
    def blog_view(request):
        return {}
        
Registers blog_view with a route named "blog" using view_blog.jinja2 template as
response.

The next views we should create are views that will handle creation and updates 
to our blog entries.

::

    @view_config(route_name='blog_action', match_param='action=create',
                 renderer='pyramid_blogr:templates/edit_blog.jinja2')
    def blog_create(request):
        return {}

Notice that there is a new keyword introduced to @view_config decorator. 

**match_params** purpose is to tell pyramid which view callable to use when our 
dynamic part of route {action} is matched, so this view will be launched for 
following URL: */blog/create*.

And then we have the view for */blog/edit* URL. 

::

    @view_config(route_name='blog_action', match_param='action=edit',
                 renderer='pyramid_blogr:templates/edit_blog.jinja2')
    def blog_update(request):
        return {}


.. note::
    Every view can be decorated unlimited times with different parameters passed 
    to @view_config, . 

Now back in `views/default.py` add::

    @view_config(route_name='auth', match_param='action=in', renderer='string',
                 request_method='POST')
    @view_config(route_name='auth', match_param='action=out', renderer='string')
    def sign_in_out(request):
        return {}

These routes will handle user authentication and logout. They are not using any 
template because they will just perform HTTP redirects.

Note that this view is decorated more than once, also it introduces one new 
parameter.

**request_method** just restricts view resolution to specific request method,
this route will not be reachable with GET requests.

.. hint::
    if you navigate your browser directly to /sign/in - you will get a 404 page, 
    because this view is not matched for GET requests.

At this point we can start implementing our view code.

Next :doc:`blog_models_and_views`

