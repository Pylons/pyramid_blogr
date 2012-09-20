=========================
2. Create database models
=========================

At this point we should create our models. In a nutshell models are representing 
data and it's underlaying storage mechanisms in application. 

We will use a relational database and  sqlalchemy ORM layer to access our data.

The default pyramid scaffold provides an example model class *MyModel* that 
we don't need - so we first need to remove whole of it.

Our application will consist of two tables:

    * **users** - stores all user for our application
    * **entries** - stores our blog entries

We should assume that our users might use some non-english characters, so we 
need to import Unicode datatype from sqlalchemy, we will also need DateTime 
field to timestamp our blog entries.

We also need to import some helper modules to generate our slugs, 
add pagination, and print nice dates - they will all come from excellent 
webhelpers package - so the top of models.py should look like this::

    import datetime <- will be used to set default dates on models
    from sqlalchemy import (
        Column,
        Integer,
        Text,
        Unicode,    <- will provide unicode field,
        UnicodeText,<- will provide unicode text text,
        DateTime    <- time abstraction field
        )
        
    from webhelpers.text import urlify <- will generate slugs
    from webhelpers.paginate import PageURL_WebOb, Page <- provides pagination
    from webhelpers.date import time_ago_in_words <- human friendly dates

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
to interact with database and persist our changes to database. 
It is thread-safe meaning that it will handle multiple requests at same time 
in a safe way, and our code from different views will not impact other requests.
It will also open and close database connections for us transparently when 
needed.
 
Also a registered zope transaction extension that will work with 
pyramid_tm (transaction manager).

What does transaction manager do?
---------------------------------

**WHOA THIS SOUNDS LIKE SCARY MAGIC!!**

.. hint ::
    It's not.

Ok, so while it might sound complicated - in practice it's very simple and 
saves developer a lot of headaches managing transactions inside application.

How it works:

* A transaction is started when browser request invokes our view code
* Some operations take place, for example database rows are inserted/updated 
  in our favorite datastore
  
  * everything went fine - we don't need to commit our transaction explictly,
    transaction manager will do this for us 
  * some unhandled exception occured, at this point we usually want to roll 
    back all the changes/queries that were sent to our datastore - transaction 
    manager will handle this for us 

What are the implications of this?

Imagine you have an application that sends a confirmation email, every time 
user registers. User inputs the data, we send him a nice welcome email and  
maybe an activation link, but during registration flow something unexpected 
happens and the code errored out.

It is very common in this situation that the user would get a welcome email, 
but in reality his profile was never persisted in database.
With packages like **pyramid_mailer** it is perfectly possible to delay email 
sending **after** the user got successfully saved in database.

Nice, huh?

But this is a more advanced topic not covered in this tutorial, the most simple 
explanation is that transaction manager will make sure our data gets correctly 
saved if everything went fine and if an error occurs - our datastore 
modifications are rolled back.


Adding model definitions
------------------------

.. hint ::
    This will make the app error out and prevent it from starting till we reach the last 
    point of current step and fix imports in other files. 
    It's perfectly normal and don't worry about this. 

We will need two declarations of models that will replace *MyModel* class ::

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(Unicode(255), unique=True, nullable=False)
        password = Column(Unicode(255), nullable=False)
        last_logged = Column(DateTime, default=datetime.datetime.utcnow)
        
    class Entry(Base):
        __tablename__ = 'entries'
        id = Column(Integer, primary_key=True)
        title = Column(Unicode(255), unique=True, nullable=False)
        body = Column(UnicodeText, default=u'')
        created = Column(DateTime, default=datetime.datetime.utcnow)
        edited = Column(DateTime, default=datetime.datetime.utcnow)

Update initialization script
----------------------------

It's time to update our database initialization script to mirror the changes in
models.py.

For this we need to open */pyramid_blogr/scripts/initializedb.py* - this is the 
file that actually gets executed when we run *initialize_pyramid_blogr_db*.

Since MyModel model is now gone we want to replace::


    with transaction.manager:
        model = MyModel(name='one', value=1)
        DBSession.add(model)

with::

    with transaction.manager:
        admin = User(username=u'admin', password=u'admin')
        DBSession.add(admin)

When you initialize a fresh database this will populate it with a single user, 
with both login and unencrypted password equal to admin.

.. warning ::
    This is just a tutorial example and **production code should utilize 
    passwords hashed with a strong one-way encryption function**. 
    You can use a package like **cryptacular** for this purpose.

The last step is to fix the imports from MyModel to User model.

.. warning ::

    Remember to replace the imports of MyModel class in 
    */pyramid_blogr/scripts/initializedb.py* **and** */pyramid_blogr/views.py*,
    otherwise your app will not start because of failed imports.

Since we don't want any initial scaffold code in our view lets remove whole 
view code from view.py and only keep the imports.    
            
Our application should start again if we try running the server. In case you 
have problems starting the application, below you can see complete source code 
of the files we modifed so far. 

.. toctree::

   basic_models_src