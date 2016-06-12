.. _blogr_project_structure:

==============================================
1. Create your pyramid_blogr project structure
==============================================

.. note::

  At the time of writing, 1.7 was the most recent stable version of Pyramid.
  You can use newer versions of Pyramid, but there may be some slight
  differences in default project templates.

When we installed Pyramid, several scripts were installed in your virtual
environment including:

* ``pcreate`` - Used to create a new project and directory structures from
  Pyramid scaffolds (project templates) shipped with Pyramid.
* ``pserve`` - Used to start a WSGI server.

Using the ``pcreate`` script, we will create our project using the alchemy
scaffold, which will provide SQLAlchemy as our default ORM layer.

.. code-block:: bash

    $ $VENV/bin/pcreate -s alchemy pyramid_blogr

We will end up with the directory ``pyramid_blogr`` which should have the
structure as explained below.

.. code-block:: text

    pyramid_blogr/
    ├── __init__.py <- main file that will configure and return WSGI application
    ├── models      <- model definitions aka data sources (often RDBMS or noSQL)
    │   ├── __init__.py
    │   ├── meta.py
    │   └── mymodel.py
    ├── routes.py
    ├── scripts/    <- util Python scripts
    │   ├── __init__.py
    │   └── initializedb.py
    ├── static/     <- usually css, js, images
    │   ├── pyramid-16x16.png
    │   ├── pyramid.png
    │   └── theme.css
    ├── templates/  <- template files
    │   ├── 404.jinja2
    │   ├── layout.jinja2
    │   └── mytemplate.jinja2
    ├── tests.py    <- tests
    └── views       <- views aka business logic
    │   ├── __init__.py
    │   ├── default.py
    │   └── notfound.py


.. _adding_dependencies:

Adding dependencies to the project
==================================

Since Pyramid tries its best to be a non-opinionated solution, we will have to
decide which libraries we want for form handling and template helpers. For this
tutorial, we will use the WTForms library and ``webhelpers2`` package.

To make them dependencies of our application, we need to open the ``setup.py``
file and extend the ``requires`` section with additional packages. In the end,
it should look like the following.

.. code-block:: ini


    requires = [
        'pyramid',
        'pyramid_jinja2',
        'pyramid_debugtoolbar',
        'pyramid_tm',
        'SQLAlchemy>=1.0',
        'transaction',
        'zope.sqlalchemy',
        'waitress',
        'wtforms==2.1',  # form library
        'webhelpers2==2.0', # various web building related helpers
        'paginate==0.5.4', # pagination helpers
        'paginate_sqlalchemy==0.2.0'
        ]

Now we can setup our application for development and add it to our environment
path. Change directory to the root of our project where ``setup.py`` lives, and
install the dependencies in ``setup.py`` with the following commands.

.. code-block:: bash

    $ cd pyramid_blogr
    $ $VENV/bin/pip install -e .

.. warning::

    Don't forget to add the period (``.``) after the ``-e`` switch.

This will install all the requirements for our application, making it
importable into our Python environment.

Another side effect of this command is that our environment gained another
command called **initialize_pyramid_blogr_db**, we will use it to create and
populate the database from the models we will create in a moment. This script
will also create the default user for our application.

.. _running-our-application:

Running our application
=======================

To visit our application, we need to use a WSGI server that will start serving
the content to the browser with following command.

.. code-block:: bash

    $ $VENV/bin/pserve --reload development.ini

This will launch an instance of a WSGI server (waitress by default) that will
run both your application code and static files. The file ``development.ini``
is used to provide all the configuration details. The ``--reload`` parameter
tells the server to restart our application every time its code changes. This
is a very useful setting for fast development and testing changes to our app
with live reloading.

.. code-block:: bash

    $ $VENV/bin/pserve --reload development.ini

    Starting subprocess with file monitor
    Starting server in PID 8517.
    serving on http://0.0.0.0:6543

You can open a web browser and visit the URL http://localhost:6543/ to see how
our application looks.

Unfortunately you will see something like the following instead of a webpage.

.. code-block:: text

    Pyramid is having a problem using your SQL database.  The problem...

This is where the ``initialize_pyramid_blogr_db`` command comes into play; but
before we run it, we need to create our application models.

Stop the WSGI server with ``CTRL-C``, then proceed to the next section in the
tutorial, :doc:`basic_models`.
