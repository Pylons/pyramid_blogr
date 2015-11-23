=====================
3. Application routes
=====================

This is the point where we want to define our routes that will be used to map
view callables to request paths.

URL dispatch provides a simple way to map URLs to view code using a simple
pattern matching language.

Our application will consist of a few sections:

* index page that will list all of our sorted blog entries
* a sign in/sign out section that will be used for authentication
* a way to create and edit our blog posts

Our URLs will look like the following.

To sign in users::

    /sign/in

When a user visits ``http://somedomain.foo/sign/in``, the view callable
responsible for signing in the user based on POST variables from the request
will be executed.

To sign out users::

    /sign/out

The index page (this was already defined via the alchemy scaffold we used
earlier, under the name "home")::

    /

Create new, or edit existing blog entries::

    /blog/{action}

You probably noticed that this URL appears unusual.  The ``{action}`` part in
the matching pattern determines that this part is dynamic, so our URL could
look like any of the following::

    /blog/create
    /blog/edit
    /blog/foobar

This single route could map to different views.

Finally a route used to view our blog entries::

    /blog/{id:\d+}/{slug}

This route constists of two dynamic parts, ``{id:\\d+}`` and ``{slug}``.

The ``:\d+`` pattern means that the route will only match digits.  So an URL
where the first dynamic part consists of only digits like the following would
be matched::

    /blog/156/Some-blog-entry

But the below example would not be matched, because the first dynamic part
contains a non-digit character::

    /blog/something/Some-blog-entry


Basics of Pyramid configuration
-------------------------------

Now that we know what routes we want, we should add them to our application.

Pyramid's ``config`` object will store our routes. To do so, we will need to
modify the file ``__init__.py`` in the root of our project. This is the central
point where initial application configuration is performed at runtime.

The ``main`` function will accept a parsed ``ini`` file that we pass to our
``pserve`` command.  Let's quickly go over what the ``main`` function does.

.. literalinclude:: src/basic_models/__init__.py
    :language: python
    :linenos:
    :lines: 13-15
    :lineno-start: 13

The above lines read the settings for SQLAlchemy, and configure the connection
engine and session maker objects.

.. literalinclude:: src/basic_models/__init__.py
    :language: python
    :linenos:
    :lines: 16
    :lineno-start: 16

The above line creates the configurator.  When needed we will be able to access
it in our views via the request object as ``request.registry.settings``.

.. literalinclude:: src/basic_models/__init__.py
    :language: python
    :linenos:
    :lines: 17
    :lineno-start: 17

The above line configures ``pyramid_jinja2`` as the template binding for
rendering our views.

.. literalinclude:: src/basic_models/__init__.py
    :language: python
    :linenos:
    :lines: 18-19
    :lineno-start: 18

In the above, two routes are added:

* a **static route** that starts with ``/static``.  This route will serve all
  our static files like JavaScript, CSS, and images.  When a browser makes a
  request to ``/static/some/resource.foo``, our application will check if
  ``/some/resource.foo`` resource is present in our static directory, and if
  it's there then it will get served to browser.

* a **view route** called ``home`` that maps to the path ``/``.

.. literalinclude:: src/basic_models/__init__.py
    :language: python
    :linenos:
    :lines: 20
    :lineno-start: 20

The above runs the scan process which will scan our entire project and load all
decorators and includes, and add them to our ``config`` object.

.. literalinclude:: src/basic_models/__init__.py
    :language: python
    :linenos:
    :lines: 21
    :lineno-start: 21

The above returns an instance of a WSGI app to the server.


Adding routes to the application configuration
----------------------------------------------

Let's add our routes to the configurator immediately after the ``home`` route
in our ``__init__.py`` at the root of our project.

.. literalinclude:: src/routes/__init__.py
    :language: python
    :linenos:
    :lines: 19-22
    :lineno-start: 19
    :emphasize-lines: 2-4

Now we are ready to develop views.

Next: :doc:`initial_views`.
