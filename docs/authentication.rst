=================
8. Authentication
=================

Great, we secured our views, but now no one can add new entries to our
application.  The finishing touch is to implement our authentication views.


Create a sign-in/sign-out form
==============================

First we need to add a login form to our existing ``index.jinja2`` template as
shown by the emphasized lines.

.. literalinclude:: src/authentication/templates/index.jinja2
    :language: jinja
    :linenos:
    :lines: 1-22
    :lineno-start: 1
    :emphasize-lines: 5-20

Now the template first checks if we are logged in.  If we are logged in, it
greets the user and presents a sign-out link.  Otherwise we are presented with
the sign-in form.


Update ``User`` model
=====================

Now it's time to update our ``User`` model.

Lets update our model with two methods: ``verify_password`` to check user input
with a password associated with the user instance, and ``by_name`` that will
fetch our user from the database, based on login.

Add the following method to our ``User`` class in ``models/user.py``.

.. literalinclude:: src/authentication/models/user.py
    :language: python
    :linenos:
    :lines: 16-
    :lineno-start: 16
    :emphasize-lines: 2-4

We also need to create the ``UserService`` class in a new file
``services/user.py``.

.. literalinclude:: src/authentication/services/user.py
    :language: python
    :linenos:

.. warning::

    In a real application, ``verify_password`` should use some strong one-way
    hashing algorithm like ``bcrypt`` or ``pbkdf2``.  Use a package like
    ``passlib`` or ``cryptacular`` which use strong hashing algorithms for
    hashing of passwords.


Update views
============

The final step is to update the view that handles authentication.

First we need to add the following import to ``views/default.py``.

.. literalinclude:: src/authentication/views/default.py
    :language: python
    :linenos:
    :lines: 1-5
    :lineno-start: 1
    :emphasize-lines: 2-4

Those functions will return HTTP headers which are used to set our ``AuthTkt``
cookie (from ``AuthTktAuthenticationPolicy``) in the user's browser.
``remember`` is used to set the current user, whereas "forget" is used to sign
out our user.

Now we have everything ready to implement our actual view.

.. literalinclude:: src/authentication/views/default.py
    :language: python
    :linenos:
    :lines: 18-
    :lineno-start: 18
    :emphasize-lines: 2-

This is a very simple view that checks if a database row with the supplied
username is present in the database.  If it is, a password check against the
username is performed.  If the password check is successful, then a new set of
headers (which is used to set the cookie) is generated and passed back to the
client on redirect.  If the username is not found, or if the password doesn't
match, then a set of headers meant to remove the cookie (if any) is issued.


Current state of our application
================================

For convenience here are the files you edited in their entirety
(``services/user.py`` was already rendered above).


``templates/index.jinja2``
--------------------------

.. literalinclude:: src/authentication/templates/index.jinja2
    :language: jinja
    :linenos:


``models/user.py``
------------------

.. literalinclude:: src/authentication/models/user.py
    :language: python
    :linenos:


``views/default.py``
--------------------

.. literalinclude:: src/authentication/views/default.py
    :language: python
    :linenos:

**Voilà!**

You can now sign in and out to add and edit blog entries using the login
``admin`` with password ``admin`` (this user was added to the database during
the ``initialize_db`` step).  But we have a few more steps to complete this
project.

Next: :doc:`registration`.
