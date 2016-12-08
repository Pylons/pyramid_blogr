========================
5. Blog models and views
========================

Models
------

Since our stubs are in place, we can start developing blog related code.

Let's start with models. Now that we have them, we can create some service
classes, and implement some methods that we will use in our views and
templates.

Create a new directory ``services/``. Inside of that, create two new
empty files, ``__init__.py`` and ``blog_record.py``. These files comprise a new
subpackage.

We will leave ``__init__.py`` empty.

Open ``services/blog_record.py``. Import some helper modules to generate
our slugs, add pagination, and print nice dates. They all come from the
excellent ``webhelpers2`` package.  Add the following imports at the top of
``blog_record.py``.

.. literalinclude:: src/blog_models_and_views/services/blog_record.py
    :linenos:
    :lines: 1-3

Next we need to create our ``BlogRecordService`` class with methods as follows.

.. literalinclude:: src/blog_models_and_views/services/blog_record.py
    :linenos:
    :lines: 6-11
    :lineno-start: 6

The method ``all`` will return a query object that can return an entire dataset
when needed.

The query object will sort the rows by date in descending order.

.. literalinclude:: src/blog_models_and_views/services/blog_record.py
    :linenos:
    :lines: 13-16
    :lineno-start: 13

The above method will return either a single blog entry by id or the ``None``
object if nothing is found.

.. literalinclude:: src/blog_models_and_views/services/blog_record.py
    :linenos:
    :lines: 18-
    :lineno-start: 18

The ``get_paginator`` method will return a paginator object that returns the
entries from a specific "page" of records from a database resultset. It will
add ``LIMIT`` and ``OFFSET`` clauses to our query based on the value of
``items_per_page`` and the current page number.

Paginator uses the wrapper ``SqlalchemyOrmPage`` which will attempt to generate
a paginator with links.  Link URLs will be constructed using the function
``url_maker`` which uses the request object to generate a new URL from the
current one, replacing the page query parameter with the new value.

Your project structure should look like this at this point.

::

    pyramid_blogr/
    ......
    ├── services      <- they query the models for data
    │     ├── __init__.py
    │     └── blog_record.py
    ......

Now it is time to move up to the parent directory, to add imports and
properties to ``models/blog_record.py``.

.. literalinclude:: src/blog_models_and_views/models/blog_record.py
    :linenos:
    :lines: 10-11
    :lineno-start: 10

Then add the following method to the class ``BlogRecord``.

.. literalinclude:: src/blog_models_and_views/models/blog_record.py
    :linenos:
    :lines: 21-23
    :lineno-start: 21

This property of entry instance will return nice slugs for us to use in URLs.
For example, pages with the title of "Foo Bar Baz" will have URLs of
"Foo-Bar-Baz". Also non-Latin characters will be approximated to their closest
counterparts.

Next add another method.

.. literalinclude:: src/blog_models_and_views/models/blog_record.py
    :linenos:
    :lines: 25-
    :lineno-start: 25

This property will return information about when a specific entry was created
in a human-friendly form, like "2 days ago".


Index view
----------

First lets add our ``BlogRecord`` service to imports in ``views/default.py``.

.. literalinclude:: src/blog_models_and_views/views/default.py
    :linenos:
    :lines: 2
    :lineno-start: 2

Now it's time to implement our actual index view by modifying our view
``index_page``.

.. literalinclude:: src/blog_models_and_views/views/default.py
    :linenos:
    :lines: 5-10
    :lineno-start: 5

We first retrieve from the URL's request object the page number that we want to
present to the user. If the page number is not present, it defaults to 1.

The paginator object returned by ``BlogRecord.get_paginator`` will then be used
in the template to build a nice list of entries.

.. note::

    Everything we return from our views in dictionaries will be available in
    templates as variables. So if we return ``{'foo':1, 'bar':2}``, then we
    will be able to access the variables inside the template directly as
    ``foo`` and ``bar``.


Index view template
-------------------

First rename ``mytemplate.jinja2`` to ``index.jinja2``.

Lets now go over the contents of the file ``layout.jinja2``,
a template file that will store a "master" template that from which other view
templates will inherit. This template will contain the page header and footer
shared by all pages.

.. literalinclude:: src/blog_models_and_views/templates/layout.jinja2
    :language: jinja
    :linenos:
    :emphasize-lines: 17,36

.. note::

    The ``request`` object is always available inside your templates namespace.

Inside your template, you will notice that we use the method
``request.static_url`` which will generate correct links to your static assets.
This is handy when building apps using URL prefixes.

In the middle of the template, you will also notice the tag
``{% block content %}``.  After we render a template that inherits from our
layout file, this is the place where our index template (or others for other
views) will appear.

Now let's open ``index.jinja2`` and put this content in it:

.. literalinclude:: src/blog_models_and_views/templates/index.jinja2
    :language: jinja
    :linenos:
    :emphasize-lines: 1,19,27

This template ``extends`` or inherits from ``layout.jinja2``, which means that
its contents will be wrapped by the layout provided by the parent template.

``{{paginator.pager()}}`` will print nice paginator links.  It will only show
up if you have more than 5 blog entries in the database.  The ``|safe`` filter
marks the output as safe HTML so jinja2 knows it doesn't need to escape any
HTML code outputted by the ``pager`` class.

``request.route_url`` is used to generate links based on routes defined in our
project. For example::

    {{request.route_url('blog_action',action='create')}} -> /blog/create


Blog view
---------

Time to update our blog view.  Near the top of ``views/blog.py``, let's add the
following imports

.. literalinclude:: src/blog_models_and_views/views/blog.py
    :language: python
    :linenos:
    :lines: 2-4
    :lineno-start: 2

Those HTTP exceptions will be used to perform redirects inside our apps.

* ``HTTPFound`` will return a 302 HTTP code response. It can accept an argument
  ``location`` that will add a ``Location:`` header for the browser.  We will
  perform redirects to other pages using this exception.
* ``HTTPNotFound`` on the other hand will just make the server serve a standard
  404 Not Found response.

Continue editing ``views/blog.py``, by modifying the ``blog_view`` view.

.. literalinclude:: src/blog_models_and_views/views/blog.py
    :language: python
    :linenos:
    :lines: 7-14
    :lineno-start: 7

This view is very simple.  First we get the ``id`` variable from our route.  It
will be present in the ``matchdict`` property of the request object.  All of
our defined route arguments will end up there.

After we get the entry id, it will be passed to the ``BlogRecord`` class method
``by_id()`` to fetch a specific blog entry.  If it's found, we return the
database row for the template to use, otherwise we present the user with a
standard 404 response.


Blog view template
------------------

Create a new file to use as the template for blog article presentation, named
``view_blog.jinja2``, with the following content.

.. literalinclude:: src/blog_models_and_views/templates/view_blog.jinja2
    :language: jinja
    :linenos:
    :emphasize-lines: 13

The ``_query`` argument introduced here for the URL generator is a list of
key/value tuples that will be used to append as GET (query) parameters,
separated by a question mark "?".  In this case, the URL will be appended by
the GET query string of ``?id=X``, where the value of ``X`` is the id of the
specific blog post to retrieve.

If you start the application now, you will get an empty welcome page stating
that "No blog entries are found".


File contents
-------------

Here are the entire file contents up to this point, except for those already
provided in their entirety.


services/blog_record.py
~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: src/blog_models_and_views/services/blog_record.py
    :linenos:


models/blog_record.py
~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: src/blog_models_and_views/models/blog_record.py
    :linenos:


views/default.py
~~~~~~~~~~~~~~~~

.. literalinclude:: src/blog_models_and_views/views/default.py
    :linenos:


views/blog.py
~~~~~~~~~~~~~

.. literalinclude:: src/blog_models_and_views/views/blog.py
    :language: python
    :linenos:


Next: :doc:`blog_create_and_update_view`.
