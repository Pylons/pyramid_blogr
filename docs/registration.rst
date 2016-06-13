.. _blogr_registration:

===============
9. Registration
===============

Now we have a basic functioning application, but we have only one hardcoded
administrator user that can add and edit blog entries.  We can provide a
registration page for new users, too.

Then we need to to provide a quality hashing solution so we can store secure
password hashes instead of clear text.  This functionality will be provided by
``passlib``.


Create the registration class, route, and form
==============================================

We should create a form to handle registration requests.  Let's open
``forms.py`` at the root of our project, and edit an import at the top of the
files and add a new form class at the end as indicated by the emphasized lines.

.. literalinclude:: src/registration/forms.py
    :language: python
    :linenos:
    :lines: 1-2
    :lineno-start: 1
    :emphasize-lines: 2

.. literalinclude:: src/registration/forms.py
    :language: python
    :linenos:
    :lines: 18-
    :lineno-start: 18
    :emphasize-lines: 1-

Our second step will be adding a new route that handles user registration in
 ``routes.py`` file as shown by the emphasized line.

.. literalinclude:: src/registration/routes.py
    :language: python
    :linenos:
    :lines: 7-
    :lineno-start: 7
    :emphasize-lines: 2

We should add a link to the registration page in our ``templates/index.jinja2``
template so we can easily navigate to it as shown by the emphasized line.

.. literalinclude:: src/registration/templates/index.jinja2
    :language: jinja
    :linenos:
    :lines: 19-21
    :lineno-start: 19
    :emphasize-lines: 2


Create the registration view
============================

At this point we have the form object and routing set up.  We are missing a
related view, model, and template code.  Let us move forward with the view code
in ``views/default.py``.

First we need to import our form definition user model at the top of the file
as shown by the emphasized lines.

.. literalinclude:: src/registration/views/default.py
    :language: python
    :linenos:
    :lines: 5-7
    :lineno-start: 5
    :emphasize-lines: 2-4

Then we can start implementing our view logic by adding the following lines to
the end of the file.

.. literalinclude:: src/registration/views/default.py
    :language: python
    :linenos:
    :lines: 34-39
    :lineno-start: 34
    :emphasize-lines: 1-

.. literalinclude:: src/registration/views/default.py
    :language: python
    :linenos:
    :lines: 41-
    :lineno-start: 41
    :emphasize-lines: 1-

Next let's create a new registration template called
``templates/register.jinja2`` with the following content.

.. literalinclude:: src/registration/templates/register.jinja2
    :language: jinja
    :linenos:


Hashing passwords
=================

Our users can now register themselves and are stored in the database using
unencrypted passwords (which is a really bad idea).

This is exactly where ``passlib`` comes into play.  We should add it to our
project's requirements in ``setup.py`` at the root of our project.

.. code-block:: python

    requires = [
        ...
        'paginate==0.5', # pagination helpers
        'paginate_sqlalchemy==0.2.0',
        'passlib'
    ]

Now we can run either command ``pip install passlib`` or ``python setup.py
develop`` to pull in the new dependency of our project.  Password hashing can
now be implemented in our ``User`` model class.

We need to import the hash context object from ``passlib`` and alter the
``User`` class to contain new versions of methods ``verify_password`` and
``set_password``.  Open ``models/user.py`` and edit it as indicated by the
emphasized lines.

.. literalinclude:: src/registration/models/user.py
    :language: python
    :linenos:
    :lines: 11-21
    :lineno-start: 11
    :emphasize-lines: 1-2,10-

.. literalinclude:: src/registration/models/user.py
    :language: python
    :linenos:
    :lines: 26-
    :lineno-start: 22
    :emphasize-lines: 1-

The last step is to alter our ``views/default.py`` to set the password, as
shown by the emphasized lines.

.. literalinclude:: src/registration/views/default.py
    :language: python
    :linenos:
    :lines: 40-44
    :lineno-start: 40
    :emphasize-lines: 1

Now our passwords are properly hashed and can be securely stored.

If you tried to log in with ``admin/admin`` credentials, you may notice that
the application threw an exception ``ValueError: hash could not be identified``
because our old clear text passwords are not identified.  So we should allow
our application to migrate to secure hashes (usually strong sha512_crypt if we
are using the quick start class).

We can easly fix this by altering our ``verify_password`` method in
``models/user.py``.

.. literalinclude:: src/registration/models/user.py
    :language: python
    :linenos:
    :lines: 21-26
    :lineno-start: 21
    :emphasize-lines: 2-5

Keep in mind that for proper migration of valid hash schemes, ``passlib``
provides a mechanism you can use to quickly upgrade from one scheme to another.


Current state of our application
================================

For convenience here are the files you edited in their entirety, with edited
lines emphasized.  Files already rendered in their entirety are omitted.


``forms.py``
------------

.. literalinclude:: src/registration/forms.py
    :language: python
    :linenos:
    :emphasize-lines: 2,18-21


``__init__.py``
---------------

.. literalinclude:: src/registration/__init__.py
    :language: python
    :linenos:
    :emphasize-lines: 32


``templates/index.jinja2``
--------------------------

.. literalinclude:: src/registration/templates/index.jinja2
    :language: jinja
    :linenos:
    :emphasize-lines: 20


``views/default.py``
--------------------

.. literalinclude:: src/registration/views/default.py
    :language: python
    :linenos:
    :emphasize-lines: 6-8,33-


``models/user.py``
------------------

.. literalinclude:: src/registration/models/user.py
    :language: python
    :linenos:
    :emphasize-lines: 12-13,22-


Next: :doc:`summary`.
