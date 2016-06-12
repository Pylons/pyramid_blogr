.. _blogr_basic_models:

=========================
2. Create database models
=========================

At this point we should create our models. In a nutshell, models represent data
and its underlying storage mechanisms in an application.

We will use a relational database and SQLAlchemy's ORM layer to access our
data.

Create and edit ``models/user.py``
----------------------------------

Our application will consist of two tables:

    * **users** - stores all users for our application
    * **entries** - stores our blog entries

We should assume that our users might use some Unicode characters, so we need
to import the Unicode datatype from SQLAlchemy. We will also need a DateTime
field to timestamp our blog entries.

Let's first create ``models/user.py``.

.. code-block:: bash

    $ touch pyramid_blogr/models/user.py

Add the following code to ``models/user.py``.

.. literalinclude:: src/basic_models/models/user.py
    :language: python
    :linenos:
    :lines: 1-9
    :lineno-start: 1

Make a copy of ``models/user.py`` as ``models/blog_record.py``. We will need
these imports in both modules.

.. code-block:: bash

    $ cp pyramid_blogr/models/user.py pyramid_blogr/models/blog_record.py

The ``alchemy`` scaffold in Pyramid provides an example model class ``MyModel``
that we don't need, as well as code that creates an index, so let's remove the
file ``models/mymodel.py``.

.. code-block:: bash

    $ rm pyramid_blogr/models/mymodel.py

Now our project structure should look like this.

.. code-block:: text

    pyramid_blogr/
    ......
    ├── models      <- model definitions aka data sources (often RDBMS or noSQL)
    │     ├── __init__.py <- database engine initialization
    │     ├── blog_record.py
    │     ├── meta.py <- database sqlalchemy metadata object
    │     └── user.py
    ......


Database session management
===========================

.. note::

    To learn how to use SQLAlchemy, please consult its `Object Relational
    Tutorial <http://docs.sqlalchemy.org/en/latest/orm/tutorial.html>`_.

If you are new to SQLAlchemy or ORM's, you are probably wondering what the
code from ``models/__init__.py``  does.

To explain we need to start reading it from the ``includeme()`` part.

.. literalinclude:: src/basic_models/models/__init__.py
    :language: python
    :linenos:
    :lines: 52-73
    :lineno-start: 52
    :emphasize-lines: 2

The first line defines a special function called ``includeme`` it will be
picked up by pyramid on runtime and will ensure that on every request, the
request object will have a ``dbsession`` propery attached that will point to
SQLAlchemy's **session object**.

The function also imports ``pyramid_tm`` - it is Pyramid's transaction manager
that will be attached to our request object as `tm` property, it will be
managing our ``dbsession`` objects behavior.

We will use it to interact with the database and persist our changes to the
database. It is thread-safe, meaning that it will handle multiple requests
at the same time in a safe way, and our code from different views will not
impact other requests. It will also open and close database connections for
us transparently when needed.

What does transaction manager do?
---------------------------------

**WHOA THIS SOUNDS LIKE SCARY MAGIC!!**

.. note::

    It's not.

OK, so while it might sound complicated, in practice it's very simple and saves
a developer a lot of headaches with managing transactions inside an
application.

Here's how the transaction manager process works:

* A transaction is started when a browser request invokes our view code.
* Some operations take place; for example, database rows are inserted or
  updated in our datastore.

  * If everything went fine, we don't need to commit our transaction explictly;
    the transaction manager will do this for us.
  * If some unhandled exception occurred, we usually want to roll back all the
    changes and queries that were sent to our datastore; the transaction
    manager will handle this for us.


What are the implications of this?
----------------------------------

Imagine you have an application that sends a confirmation email every time a
user registers. A user, Nephthys, inputs the data to register, and we send
Nephthys a nice welcome email and maybe an activation link, but during
registration flow, something unexpected happens and the code errors out.

It is very common in this situation that the user would get a welcome email,
but in reality their profile was never persisted in the database. With packages
like **pyramid_mailer** it is perfectly possible to delay email sending until
**after** the user's information is successfully saved in the database.

Nice, huh?

Although this is a more advanced topic not covered in depth in this tutorial,
the most simple explanation is that the transaction manager will make sure our
data gets correctly saved if everything went smoothly, and if an error occurs
then our datastore modifications are rolled back.


Adding model definitions
========================

.. note::

    This will make the application error out and prevent it from starting until
    we reach the last point of the current step and fix imports in other files.
    It's perfectly normal, so don't worry about immediate errors.

We will need two declarations of models that will replace the ``MyModel`` class
that was created when we scaffolded our project.

After the import part in ``models/user.py`` add the following.


.. literalinclude:: src/basic_models/models/user.py
    :language: python
    :linenos:
    :lines: 11-16
    :lineno-start: 11

After the import part in ``models/blog_record.py`` add the following.

.. literalinclude:: src/basic_models/models/blog_record.py
    :language: python
    :linenos:
    :lines: 11-17

Now it's time to update our ``models/__init__.py`` to include our models. This
is especially handy because it ensures that SQLAlchemy mappers will pick up all
of our model classes and functions, like ``create_all``, and that the models
will do what you expect.

Add these imports to the file (remember to also remove the ``MyModel`` import).

.. literalinclude:: src/basic_models/models/__init__.py
    :language: python
    :linenos:
    :lines: 6-10
    :lineno-start: 6


Update database initialization script
=====================================

It's time to update our database initialization script to mirror the changes in
our ``models`` package.

Open ``scripts/initializedb.py``.  This is the file that actually gets executed
when we run ``initialize_pyramid_blogr_db``.

We will remove the ``MyModel`` and import the ``User`` model.

.. literalinclude:: src/basic_models/scripts/initializedb.py
    :language: python
    :linenos:
    :lines: 18
    :lineno-start: 18

Since the ``MyModel`` model is now gone, we want to replace the following bits:

.. code-block:: python

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        model = MyModel(name='one', value=1)
        dbsession.add(model)

with this:

.. literalinclude:: src/basic_models/scripts/initializedb.py
    :language: python
    :linenos:
    :lines: 41-45
    :lineno-start: 41
    :emphasize-lines: 4

When you initialize a fresh database, this will populate it with a single user,
with both login and unencrypted password equal to ``admin``.

.. warning::

    This is just a tutorial example and **production code should utilize
    passwords hashed with a strong one-way encryption function**.  You can use
    a package like `passlib <http://pythonhosted.org/passlib/>`_ or
    `cryptacular <https://bitbucket.org/dholth/cryptacular/>`_ for this
    purpose.

The last step to get the application running is to change ``views/default.py``
``MyModel`` class into out User model.

.. code-block:: python

    from ..models import MyModel

into changes to

.. literalinclude:: src/basic_models/views/default.py
    :language: python
    :linenos:
    :lines: 6
    :lineno-start: 6

and the query in ``my_view`` changes to:

.. literalinclude:: src/basic_models/views/default.py
    :language: python
    :linenos:
    :lines: 10-16
    :lineno-start: 12
    :emphasize-lines: 3-4

Our application should start again if we try running the server.

.. code-block:: bash

    $ $VENV/bin/pserve --reload development.ini

If you visit the URL http://0.0.0.0:6543 then you should see a
"Pyramid is having a problem ..." error message.

In case you have problems starting the application, you can see complete source
code of the files we modifed below.

``models/__init__.py``

.. literalinclude:: src/basic_models/models/__init__.py
    :linenos:

``models/user.py``

.. literalinclude:: src/basic_models/models/user.py
    :linenos:

``models/blog_record.py``

.. literalinclude:: src/basic_models/models/blog_record.py
    :linenos:

``scripts/initializedb.py``

.. literalinclude:: src/basic_models/scripts/initializedb.py
    :linenos:

``__init__.py``

.. literalinclude:: src/basic_models/__init__.py
    :linenos:

``views/default.py``

.. literalinclude:: src/basic_models/views/default.py
    :linenos:

If our application starts correctly, you should run the
``initialize_pyramid_blogr_db`` command to update the database.

.. code-block:: bash

    $ $VENV/bin/initialize_pyramid_blogr_db development.ini

Next :doc:`routes`.
