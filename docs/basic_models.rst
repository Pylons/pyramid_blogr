.. _blogr_basic_models:

=========================
2. Create database models
=========================

At this point we should create our models. In a nutshell models represent 
data and its underlaying storage mechanisms in an application. 

We will use a relational database and sqlalchemy's ORM layer to access our data.

The default pyramid scaffold provides an example model class `MyModel` that
we don't need - so we first need to remove whole of it.

In real life applications data models tend to grow over time and contain lots of additional methods.
Instead of keeping all of our models in a single file, let's create a new `models` package in our structure that 
will hold one model per file.

Now we need to move the file `models.py` to our newly created directory. Let's rename it `meta.py` to make a
python package from our `models` directory.

Our directory structure should look like this after this operation::

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

Our application will consist of two tables:

    * **users** - stores all users for our application
    * **entries** - stores our blog entries

We should assume that our users might use some non-english characters, so we 
need to import the Unicode datatype from sqlalchemy, we will also need a DateTime 
field to timestamp our blog entries.

Let's first create `models/user.py`. Let's remove the now unused import code from
`models/meta.py` and paste it into our newly created user file. While we are doing
this, let's add a few more imports to our `user.py` file.

::


    import datetime #<- will be used to set default dates on models
    from pyramid_blogr.models.meta import Base  #<- we need to import our sqlalchemy metadata for model classes to inherit from
    from sqlalchemy import (
        Column,
        Integer,
        Unicode,     #<- will provide unicode field,
        UnicodeText, #<- will provide unicode text field,
        DateTime     #<- time abstraction field,
        )


Now repeat the step and insert the same code into `models/blog_record.py`

After all operations our `models/meta.py` should only contain::

    from sqlalchemy.ext.declarative import declarative_base

    from sqlalchemy.orm import (
        scoped_session,
        sessionmaker,
    )

    from zope.sqlalchemy import ZopeTransactionExtension

    DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    Base = declarative_base()

And our project structure should look like this::

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
    └── views.py    <- views aka business logic

Database session management
---------------------------

.. hint ::
    To learn how to use sqlalchemy please consult its 
    Object Relational Tutorial: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

If you are new to sqlalchemy or ORM's you are probably wondering what this 
code does::
   
    DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    Base = declarative_base()

The first line initializes sqlalchemy's threaded **session maker** - we will use it
to interact with the database and persist our changes to the database. 
It is thread-safe meaning that it will handle multiple requests at same time 
in a safe way, and our code from different views will not impact other requests.
It will also open and close database connections for us transparently when 
needed.
 
The `extension=ZopeTransactionExtension()` we pass as a parameter to sessionmaker in
order to use the registered zope transaction extension. This will work with pyramid's
transaction manager (pyramid_tm).

What does transaction manager do?
---------------------------------

**WHOA THIS SOUNDS LIKE SCARY MAGIC!!**

.. hint ::
    It's not.

Ok, so while it might sound complicated - in practice it's very simple and 
saves a developer a lot of headaches managing transactions inside application.

How it works:

* A transaction is started when a browser request invokes our view code
* Some operations take place; for example database rows are inserted/updated 
  in our favorite datastore
  
  * if  everything went fine - we don't need to commit our transaction explictly,
    transaction manager will do this for us 
  * if some unhandled exception occured - at this point we usually want to roll 
    back all the changes/queries that were sent to our datastore - transaction 
    manager will handle this for us 

What are the implications of this?

Imagine you have an application that sends a confirmation email every time 
a user registers. A user, John, inputs the data to register, we send John a nice welcome email and  
maybe an activation link, but during registration flow something unexpected 
happens and the code errored out.

It is very common in this situation that the user would get a welcome email, 
but in reality his profile was never persisted in the database.
With packages like **pyramid_mailer** it is perfectly possible to delay email 
sending until **after** the user's information is successfully saved in the database.

Nice, huh?

But this is a more advanced topic not covered in this tutorial, the most simple 
explanation is that transaction manager will make sure our data gets correctly 
saved if everything went smoothly and if an error occurs - our datastore 
modifications are rolled back.


Adding model definitions
------------------------

.. hint ::
    This will make the app error out and prevent it from starting till we reach the last 
    point of current step and fix imports in other files. 
    It's perfectly normal, so don't worry about this. 

We will need two declarations of models that will replace the *MyModel* class that was created when we scaffolded
our project.

After the import part of `models/user.py` add the following::

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(Unicode(255), unique=True, nullable=False)
        password = Column(Unicode(255), nullable=False)
        last_logged = Column(DateTime, default=datetime.datetime.utcnow)

After the import part of `models/blog_record.py` add the following::

    class BlogRecord(Base):
        __tablename__ = 'entries'
        id = Column(Integer, primary_key=True)
        title = Column(Unicode(255), unique=True, nullable=False)
        body = Column(UnicodeText, default=u'')
        created = Column(DateTime, default=datetime.datetime.utcnow)
        edited = Column(DateTime, default=datetime.datetime.utcnow)


Now its time to update our `models/__init__.py` to include our models - this is especially handy because it ensures
that sqlalchemy mappers will pick up all our model classes and functions like `create_all` do what you expect them
to do.

Add these imports to the end of the file::

    from .user import User
    from .blog_record import BlogRecord


Update initialization script
----------------------------

It's time to update our database initialization script to mirror the changes in
models.py.

For this we need to open */pyramid_blogr/scripts/initializedb.py* - this is the 
file that actually gets executed when we run *initialize_pyramid_blogr_db*.

First remove `MyModel` import from that file and fix imports from modules package, also import `User` model::

    from ..models.meta import DBSession, Base
    from ..models import User

Since MyModel model is now gone we want to replace::

    with transaction.manager:
        model = MyModel(name='one', value=1)
        DBSession.add(model)

with::

    with transaction.manager:
        admin = User(name=u'admin', password=u'admin')
        DBSession.add(admin)

When you initialize a fresh database this will populate it with a single user, 
with both login and unencrypted password equal to admin.

.. warning ::
    This is just a tutorial example and **production code should utilize 
    passwords hashed with a strong one-way encryption function**. 
    You can use a package like **passlib** or **cryptacular** for this purpose.

The last step is to fix the imports from MyModel to User model and meta package in __init__.py.

in `pyramid_blogr/__init__.py`::

    from .models import (
        DBSession,
        Base,
        )

becomes::

    from .models.meta import (
        DBSession,
        Base,
        )

.. warning ::

    Remember to replace the imports of MyModel, DBSession classes in
    */pyramid_blogr/scripts/initializedb.py* **and** */pyramid_blogr/tests.py*,
    otherwise your app will not start because of failed imports.

Same as with models, when your application grows over time you will want to organize views into logical sections
based on their functionality. Fow now remove the `views.py` completely.
            
Our application should start again if we try running the server. In case you 
have problems starting the application, you can see complete source code 
of the files we modifed below. 

If our application starts correctly, you should run the *initialize_pyramid_blogr_db*, 
command from your environment, it may look like this::

~/yourVenv/bin/initialize_pyramid_blogr_db development.ini


Next  :doc:`routes`
