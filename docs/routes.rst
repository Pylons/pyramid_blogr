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


Adding routes to the application configuration
----------------------------------------------

Let's add our routes to the configurator immediately after the ``home`` route
in our ``routes.py`` at the root of our project.

.. literalinclude:: src/routes/__init__.py
    :language: python
    :linenos:
    :lines: 19-22
    :lineno-start: 19
    :emphasize-lines: 2-4

Now we are ready to develop views.

Next: :doc:`initial_views`.
