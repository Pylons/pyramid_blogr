=========================
Create your fresh project
=========================

First we need to install pyramid framework itself::

    pip install pyramid


This will install pyramid itself with it's base dependancies, your python 
environment (ideally VirtualEnv), will now contain some helpful commands 
including:

    * **pcreate** used to create fresh project and directory structures from 
      pyramid scaffolds(project templates) that pyramid ships with
    * **pserve** will be used to start our WSGI server

The next step is to create our project using alchemy scaffold - that will 
provide SQLAlchemy as our default ORM layer::

~/yourVenv/bin/pcreate -s alchemy pyramid_blogr

Adding dependancies to the project
----------------------------------

Since pyramid tries it's best to be a non-opinionated solution we will have to 
decide what libraries we want for form handling and template helpers.
For this tutorial we will use great WTForms library and webhelpers packages.

To make them dependancies of our application we need to open setup.py file 
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
  