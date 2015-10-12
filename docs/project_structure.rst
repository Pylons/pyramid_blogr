=========================================
1. Create your tutorial project structure
=========================================

.. hint ::
    At the time of writing, 1.5.7 was the most recent stable version 
    of Pyramid, you can use newer version of Pyramid but there will be some slight
    differences in default project templates.

First we need to install Pyramid framework itself::

    pip install pyramid==1.5.7

This will install Pyramid itself with its base dependencies, your Python 
environment (ideally VirtualEnv), will now contain some helpful commands 
including:

    * **pcreate** used to create fresh project and directory structures from 
      Pyramid scaffolds(project templates) that Pyramid ships with
    * **pserve** will be used to start our WSGI server

The next step is to create our project using alchemy scaffold - that will 
provide SQLAlchemy as our default ORM layer::

    ~/yourVenv/bin/pcreate -s alchemy pyramid_blogr

We will end up with pyramid_blogr dir that should have following structure::

    pyramid_blogr/
    ├── __init__.py <- main file that will configure and return WSGI application
    ├── models.py   <- model definitions aka data sources (often RDBMS or noSQL)
    ├── scripts/    <- util Python scripts
    ├── static/     <- usually css, js, images
    ├── templates/  <- template files
    ├── tests.py    <- tests
    └── views.py    <- views aka business logic 

Adding dependencies to the project
----------------------------------

Since Pyramid tries its best to be a non-opinionated solution we will have to 
decide what libraries we want for form handling and template helpers.
For this tutorial we will use great WTForms library and webhelpers packages.

To make them dependencies of our application we need to open setup.py file 
and extend **requires** with additional packages, in the end it should look 
like this::

    requires = [
        'pyramid==1.5.7',
        'pyramid_mako', # replaces default chameleon templates
        'pyramid_debugtoolbar',
        'pyramid_tm',
        'SQLAlchemy==1.0.8',
        'transaction',
        'zope.sqlalchemy',
        'waitress',
        'wtforms==2.0.2',  # form library
        'webhelpers2==2.0', # various web building related helpers
        'paginate==0.5', # pagination helpers
        'paginate_sqlalchemy==0.2.0'
        ]
        
Now we can setup our application for development and add it to our environment 
path. In the root of our project where setup.py lives execute following line::

    ~/yourVenv/bin/pip install -e .

This will install all the requirements for our application and will make it 
importable in our Python environment.

.. warning::
    Don't forget to add the . after -e switch

Another side effect of this command is that our environment gained another 
command called **initialize_pyramid_blogr_db**, we will use it to 
create/populate the database from the models we will create in a moment, 
this script will also create the default user for our application.

Running our application
-----------------------

To visit our application we need to use a WSGI server that will start serving 
the content to the browser with following command:: 

    ~/yourVenv/bin/pserve --reload development.ini

This will launch an instance of a WSGI (waitress by default) server that will run 
both your application code and static files.
**development.ini file is used to provide all the configuration details**, 
the *--reload* parameter tells the server to restart our application every 
time its code changes, this is a great setting for fast development and 
testing live changes to our app. 

Unfortunately on our first run the application will throw exception::

    ImportError: No module named 'pyramid_chameleon'

This is because we switched from chameleon templating engine to mako.

To fix this you need to open `pyramid_blogr/__init__.py` and change::

    config.include('pyramid_chameleon')
    # to
    config.include('pyramid_mako')

On your next application restart should see something like this::

    Starting subprocess with file monitor
    Starting server in PID 8517.
    serving on http://0.0.0.0:6543

You can open your favorite browser and go to http://localhost:6543/ to see how 
our application looks like.

Unfortunately you will see something like this instead of a webpage ;-) ::

    Pyramid is having a problem using your SQL database.  The problem...

This is where the **initialize_pyramid_blogr_db** command comes into play, but 
before we run it we need to create our application models.

Next :doc:`basic_models`
