================
4. Initial views
================

Now it's time to create our views files and add our view callables.

Every view will be decorated with a ``@view_config`` decorator.

``@view_config`` will configure our Pyramid application by telling it how to
correlate our view callables with routes, and set some restrictions on specific
view resolution mechanisms.  It gets picked up when ``config.scan()`` is called
in our ``__init__.py``, and all of our views are registered with our app.

.. note::

    You could explictly configure your application with the
    ``config.add_view()`` method, but the approach with ``@view_config`` and
    ``config.scan()`` is often more convenient.


Edit our ``views`` files
========================

Let's make some stubs for our views.  We will populate them with actual code in
later chapters.

Open ``views/default.py`` and add the following.

.. literalinclude:: src/initial_views/views/default.py
    :language: python
    :linenos:
    :lines: 1-7

Here ``@view_config`` takes two parameters that will register our
``index_page`` callable in Pyramid's registry, specifying the route that should
be used to match this view.  We also specify the renderer that will be used to
transform the data which the view returns into a response suitable for the
client.

The template location is specified using the *asset location* format, which is
in the form of *package_name:path_to_template*, or by specifying relative
path to the template.

.. note::

    It also easy to add your own custom renderer, or use an add-on package like
    `pyramid_mako
    <http://docs.pylonsproject.org/projects/pyramid-mako/en/latest/>`_.

    The renderer is picked up automatically by specifying the file extension,
    like *asset.jinja2*/*asset.jinja2* or when you provide a name, such as for
    the ``string/json`` renderer.

    Pyramid provides a few renderers including:
        * jinja2 templates (by external package)
        * mako templates (by external package)
        * chameleon templates (by external package)
        * string output
        * json encoder

Create new file ``views/blog.py`` and add the following contents:

.. literalinclude:: src/initial_views/views/blog.py
    :language: python
    :linenos:
    :lines: 1-7

This registers ``blog_view`` with a route named ``'blog'`` using the
``view_blog.jinja2`` template as the response.

The next views we should create are views that will handle creation and updates
to our blog entries.

.. literalinclude:: src/initial_views/views/blog.py
    :language: python
    :linenos:
    :lines: 10-13
    :lineno-start: 10

Notice that there is a new keyword introduced to the ``@view_config``
decorator. The purpose of ``match_param`` is to tell Pyramid which view
callable to use when the dynamic part of the route ``{action}`` is matched.
For example, the above view will be launched for the URL ``/blog/create``.

Next we add the view for the URL ``/blog/edit``.

.. literalinclude:: src/initial_views/views/blog.py
    :language: python
    :linenos:
    :lines: 16-
    :lineno-start: 16

.. note::

    Every view can be decorated unlimited times with different parameters
    passed to ``@view_config``.

Now switch back to ``views/default.py``, and add the following.

.. literalinclude:: src/initial_views/views/default.py
    :language: python
    :linenos:
    :lines: 10-
    :lineno-start: 10

These routes will handle user authentication and logout. They do not use a
template because they will just perform HTTP redirects.

Note that this view is decorated more than once. It also introduces one new
parameter. ``request_method`` restricts view resolution to a specific request
method, or in this example, to just POST requests.  This route will not be
reachable with GET requests.

.. note::

    If you navigate your browser directly to ``/sign/in``, you will get a 404
    page because this view is not matched for GET requests.

Content of ``views`` files
==========================

Here's how our ``views`` files look at this point.


``views/blog.py``
-----------------

.. literalinclude:: src/initial_views/views/blog.py
    :language: python
    :linenos:


``views/default.py``
--------------------

.. literalinclude:: src/initial_views/views/default.py
    :language: python
    :linenos:


``views/__init__.py`` is currently an empty file.

At this point we can start implementing our view code.

Next: :doc:`blog_models_and_views`.
