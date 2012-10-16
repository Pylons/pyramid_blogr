=================================================
What you will know after you finish this tutorial
=================================================

The tutorial is really simple but should be enough of a head start to writing 
applications using Pyramid Web Framework. By the end of it you should have a 
basic understanding of templating, working with databases, using url routes to 
launch our business logic(views) and authentication, example of form library 
usage and pagination of our blog entries.

Pyramid_blogr makes some initial assumptions:

* Will use **alchemy** scaffold with SQLAlchemy as its ORM layer
* **Mako** templates will be our choice for templating engine
* **URL dispatch** will be the default way for our view resolution
* A single user in database will be created in setup phase
* Will perform a simple authentication of the user
* Authenticated user will be able to make blog entries
* The entries will be listed from newest to oldest one
* We will use **webhelpers** package for pagination
* **WTForms** form library will provide form validation

This tutorial was originally created by **Marcin Lulek**, developer, freelancer 
and founder of https://errormator.com.

Documentation links
-------------------

* **Pyramid** : http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/
* **Mako templates** : http://www.makotemplates.org/
* **SQLAlchemy** : http://www.sqlalchemy.org/
* **Webhelpers** : http://webhelpers.readthedocs.org/en/latest/
* **WTForms** : http://wtforms.simplecodes.com

The complete sourcecode for this application is available at:

https://github.com/Pylons/pyramid_blogr
