.. _blogr_basic_models:

=========================
2. Create database models
=========================

At this point we should create our models. In a nutshell, models represent data
and its underlying storage mechanisms in an application.

We will use a relational database and SQLAlchemy's ORM layer to access our
data.


Using packages instead of single files
======================================

In real life applications, data models tend to grow over time and contain lots
of additional methods. Instead of keeping all of our models in a single file,
let's create a new ``models`` package in our structure that will hold one model
per file.

.. code-block:: bash

    $ mkdir pyramid_blogr/models
    $ touch pyramid_blogr/models/__init__.py

Now we need to move the file ``models.py`` in to our newly created directory.
Let's rename it ``meta.py`` to make a Python package from our ``models``
directory.

.. code-block:: bash

    $ mv pyramid_blogr/models.py pyramid_blogr/models/meta.py

Our directory structure should look like this after issuing the above commands.

.. code-block:: text

    pyramid_blogr/
    ├── __init__.py <- main file that will configure and return WSGI application
    ├── models      <- model definitions aka data sources (often RDBMS or noSQL)
    │     ├-─ __init__.py
    │     └── meta.py <- former models.py
    ├── scripts/    <- util python scripts
    ├── static/     <- usually css, js, images
    ├── templates/  <- template files
    ├── tests.py    <- tests
    └── views.py    <- views aka business logic


Edit ``models/meta.py``
-----------------------

The ``alchemy`` scaffold in Pyramid provides an example model class ``MyModel``
that we don't need, as well as code that creates an index, so let's remove the
following lines from ``meta.py``.

.. code-block:: python

    class MyModel(Base):
        __tablename__ = 'models'
        id = Column(Integer, primary_key=True)
        name = Column(Text)
        value = Column(Integer)

    Index('my_index', MyModel.name, unique=True, mysql_length=255)

We should also remove the now unused import code.

.. code-block:: python

    from sqlalchemy import (
        Column,
        Index,
        Integer,
        Text,
        )

Our ``models/meta.py`` should now only contain the following.

.. literalinclude:: src/basic_models/models/meta.py
    :linenos:


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

.. code-block:: python

    import datetime #<- will be used to set default dates on models
    from pyramid_blogr.models.meta import Base  #<- we need to import our sqlalchemy metadata from which model classes will inherit
    from sqlalchemy import (
        Column,
        Integer,
        Unicode,     #<- will provide Unicode field
        UnicodeText, #<- will provide Unicode text field
        DateTime,    #<- time abstraction field
        )

Make a copy of ``models/user.py`` as ``models/blog_record.py``. We will need
these imports in both modules.

.. code-block:: bash

    $ cp pyramid_blogr/models/user.py pyramid_blogr/models/blog_record.py

Now our project structure should look like this.

.. code-block:: text

    pyramid_blogr/
    ├── __init__.py <- main file that will configure and return WSGI application
    ├── models      <- model definitions aka data sources (often RDBMS or noSQL)
    │     ├── __init__.py
    │     ├── blog_record.py
    │     ├── meta.py <- former models.py
    │     └── user.py
    ├── scripts/    <- util python scripts
    ├── static/     <- usually css, js, images
    ├── templates/  <- template files
    ├── tests.py    <- tests
    └── views.py    <- views aka business logic


Database session management
===========================

.. note::

    To learn how to use SQLAlchemy, please consult its `Object Relational
    Tutorial <http://docs.sqlalchemy.org/en/latest/orm/tutorial.html>`_.

If you are new to SQLAlchemy or ORM's, you are probably wondering what this
code does.

.. code-block:: python

    DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    Base = declarative_base()

The first line initializes SQLAlchemy's threaded **session maker**. We will use
it to interact with the database and persist our changes to the database. It is
thread-safe, meaning that it will handle multiple requests at the same time in
a safe way, and our code from different views will not impact other requests.
It will also open and close database connections for us transparently when
needed.

The ``extension=ZopeTransactionExtension()`` is passed as a parameter to
``sessionmaker()`` in order to use the registered Zope transaction extension.
This will work with Pyramid's transaction manager, ``pyramid_tm``.


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

.. code-block:: python

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(Unicode(255), unique=True, nullable=False)
        password = Column(Unicode(255), nullable=False)
        last_logged = Column(DateTime, default=datetime.datetime.utcnow)

After the import part in ``models/blog_record.py`` add the following.

.. code-block:: python

    class BlogRecord(Base):
        __tablename__ = 'entries'
        id = Column(Integer, primary_key=True)
        title = Column(Unicode(255), unique=True, nullable=False)
        body = Column(UnicodeText, default=u'')
        created = Column(DateTime, default=datetime.datetime.utcnow)
        edited = Column(DateTime, default=datetime.datetime.utcnow)

Now it's time to update our ``models/__init__.py`` to include our models. This
is especially handy because it ensures that SQLAlchemy mappers will pick up all
of our model classes and functions, like ``create_all``, and that the models
will do what you expect.

Add these imports to the file.

.. code-block:: python

    from .user import User
    from .blog_record import BlogRecord


Update database initialization script
=====================================

It's time to update our database initialization script to mirror the changes in
our ``models`` package.

Open ``scripts/initializedb.py``.  This is the file that actually gets executed
when we run ``initialize_pyramid_blogr_db``.

We will remove the ``MyModel`` import and fix imports from the ``models``
package.  We will also import the ``User`` model.

.. code-block:: python

    from ..models.meta import DBSession, Base
    from ..models import User

Since the ``MyModel`` model is now gone, we want to replace the following bits:

.. code-block:: python

    with transaction.manager:
        model = MyModel(name='one', value=1)
        DBSession.add(model)

with this:

.. code-block:: python

    with transaction.manager:
        admin = User(name=u'admin', password=u'admin')
        DBSession.add(admin)

When you initialize a fresh database, this will populate it with a single user,
with both login and unencrypted password equal to ``admin``.

.. warning::

    This is just a tutorial example and **production code should utilize
    passwords hashed with a strong one-way encryption function**.  You can use
    a package like `passlib <http://pythonhosted.org/passlib/>`_ or
    `cryptacular <https://bitbucket.org/dholth/cryptacular/>`_ for this
    purpose.

The last step is to fix the imports in ``pyramid_blogr/__init__.py`` (at the
root of our project) to use the ``meta`` package.

Open ``pyramid_blogr/__init__.py`` and edit the import such that this:

.. code-block:: python

    from .models import (
        DBSession,
        Base,
        )

becomes:

.. code-block:: python

    from .models.meta import (
        DBSession,
        Base,
        )


Update ``tests.py``
===================

Since we updated the imports in ``models`` and ``scripts/initializebd.py``, we
need to update the import in ``pyramid_blogr/tests.py`` as well.

Open ``tests.py`` at the root of our project. Change the following line from:

.. code-block:: python

    from .models import DBSession

to:

.. code-block:: python

    from .models.meta import DBSession

.. warning::

    Remember to replace the imports of the ``MyModel`` and ``DBSession``
    classes in ``scripts/initializedb.py`` **and** ``tests.py``. Otherwise your
    app will not start because of failed imports.

.. TODO: Add sufficient details for how to modify tests.py to the above
  warning.

Same as with models, when your application grows over time, you will want to
organize views into logical sections based on their functionality. Fow now
remove the ``views.py`` file completely.

.. code-block:: bash

    $ rm views.py

Our application should start again if we try running the server.

.. code-block:: bash

    $ $VENV/bin/pserve --reload development.ini

If you visit the URL http://0.0.0.0:6543 then you should see a "404 Not Found"
error message.

In case you have problems starting the application, you can see complete source
code of the files we modifed below.

``models/__init__.py``

.. literalinclude:: src/basic_models/models/__init__.py
    :linenos:

``models/meta.py``

.. literalinclude:: src/basic_models/models/meta.py
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

``tests.py``

.. literalinclude:: src/basic_models/tests.py

If our application starts correctly, you should run the
``initialize_pyramid_blogr_db`` command to update the database.

.. code-block:: bash

    $ $VENV/bin/initialize_pyramid_blogr_db development.ini

Next :doc:`routes`.
