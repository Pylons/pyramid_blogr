======================================
Create your tutorial project structure
======================================

First we need to install pyramid framework itself::

    pip install pyramid


This will install pyramid itself with it's base dependencies, your python 
environment (ideally VirtualEnv), will now contain some helpful commands 
including:

    * **pcreate** used to create fresh project and directory structures from 
      pyramid scaffolds(project templates) that pyramid ships with
    * **pserve** will be used to start our WSGI server

The next step is to create our project using alchemy scaffold - that will 
provide SQLAlchemy as our default ORM layer::

    ~/yourVenv/bin/pcreate -s alchemy pyramid_blogr

We will end up with pyramid_blogr dir that should have following structure::

    /pyramid_blogr
        /scripts/ <- util python scripts
        /static/ <- usually css, js, images
        /templates/ <- template files
        /__init__.py <- main file that will configure and return WSGI application
        /models.py <- model definitions aka data sources (often RDBMS or noSQL)
        /views.py <- views aka business logic 

Adding dependencies to the project
----------------------------------

Since pyramid tries it's best to be a non-opinionated solution we will have to 
decide what libraries we want for form handling and template helpers.
For this tutorial we will use great WTForms library and webhelpers packages.

To make them dependencies of our application we need to open setup.py file 
and extend **requires** with additional packages, in the end it should look 
like this::

    requires = [
        'pyramid',
        'SQLAlchemy',
        'transaction',
        'pyramid_tm',
        'pyramid_debugtoolbar',
        'zope.sqlalchemy',
        'waitress',
        'wtforms',
        'webhelpers'
        ]
        
Now we can setup our application for development and add it to out environment 
path. In the root of our project where setup.py lives execute following line::

    ~/yourVenv/bin/pip install -e .

This will install all the requirements for our application and will make it 
importable in our python environment.

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
both your application code and static files, our **development.ini file is used 
to provide all the configuration details**, the *--reload* parameter tells the 
server to restart our application every time it's code changes, this is a great 
setting for fast development and testing live changes to our app. 

You should see something like this::

    Starting subprocess with file monitor
    Starting server in PID 8517.
    serving on http://0.0.0.0:6543

You can open your favorite browser and go to http://localhost:6543/ to see how 
our application looks like.

Unfortunately you will see something like this instead of a webpage ;-) ::

    Pyramid is having a problem using your SQL database.  The problem...

This is where the **initialize_pyramid_blogr_db** command comes into play, but 
before we run it we need to create our application models.