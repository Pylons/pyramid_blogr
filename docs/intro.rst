.. _introduction:

=================================================
What you will know after you finish this tutorial
=================================================

This tutorial is really simple, but it should give you enough of a head start
to writing applications using the Pyramid Web Framework. By the end of it, you
should have a basic understanding of templating, working with databases, using
URL routes to launch business logic (views), authentication, authorization,
using a form library, and usage and pagination of our blog entries.

Pyramid_blogr makes some initial assumptions:

* We will use Pyramid's **alchemy** scaffold with SQLAlchemy as its ORM layer.
* **Jinja2** templates will be our choice for templating engine.
* **URL dispatch** will be the default way for our view resolution.
* A single user in the database will be created during the setup phase.
* We will perform simple authentication of the user.
* The authenticated user will be authorized to make blog entries.
* The blog entries will be listed from newest to oldest.
* We will use the **webhelpers2** package for pagination.
* The **WTForms** form library will provide form validation.

This tutorial was originally created by **Marcin Lulek**, developer, freelancer
and founder of `app enlight <https://appenlight.com>`_.

:doc:`Start the tutorial <project_structure>`.


Documentation links
===================

* :ref:`Pyramid <pyramid:index>`
* `Jinja2 templates <http://jinja.pocoo.org/>`_
* `pyramid_jinja2 <http://docs.pylonsproject.org/projects/pyramid-jinja2/en/latest/>`_
* `SQLAlchemy <http://docs.sqlalchemy.org/en/>`_
* `Webhelpers <http://webhelpers.readthedocs.org/en/latest/>`_
* :ref:`WTForms <wtforms:doc-index>`

The complete source code for this application is available on GitHub at:

https://github.com/Pylons/pyramid_blogr


Improve this tutorial
=====================

There may be mistakes in this tutorial, and we always appreciate pull requests
to improve this tutorial.  Please use the `issue tracker on GitHub
<https://github.com/Pylons/pyramid_blogr>`_ or submit pull requests to the
project through GitHub.  Please see `contributing.md
<https://github.com/Pylons/pyramid_blogr>`_ for details.
