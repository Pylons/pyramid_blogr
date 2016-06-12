================
7. Authorization
================

At this point we have a fully working application, but you may have noticed
that anyone can alter our entries.  We should change that by introducing user
*authorization*, where we assign security statements to resources (e.g., blog
entries) describing the permissions required to perform an operation (e.g., add
or edit a blog entry).

For the sake of simplicity, in this tutorial we will assume that every user can
edit every blog entry as long as they are signed in to our application.

Pyramid provides some ready-made policies for this, as well as mechanisms for
writing custom policies.

We will use the policies provided by the framework:

* ``AuthTktAuthenticationPolicy``

  Obtains user data from a Pyramid "auth ticket" cookie.

* ``ACLAuthorizationPolicy``

  An authorization policy which consults an ACL object attached to a context to
  determine authorization information about a principal or multiple principals.

OK, so the description for ``ACLAuthorizationPolicy`` has a lot of scary words
in it, but in practice it's a simple concept that allows for great flexibility
when defining permission systems.

The policy basically checks if a user has a permission to the specific context
of a view based on Access Control Lists.


What does this mean? What is a context?
=======================================

A context could be anything.  Imagine you are building a forum application,
and you want to add a feature where only moderators will be able to edit a
specific topic in a specific forum.  In this case, our context would be the
forum object; it would have info attached to it about who has specific
permissions to this resource.

Or something simpler, who can access admin pages?  In this case, a context
would be an arbitrary object that has information attached to it about who is
an administrator of the site.


How does this relate to our application?
========================================

Since our application does not track who owns blog entries, we will assume the
latter scenario: any authenticated (logged in) user has authorization to
administer the blog entries.  We will make the most trivial context factory
object.  As its name implies, the factory will return the context object (in
our case, an arbitrary class).  It will say that *everyone logged in* to our
application can create and edit blog entries.


Create a context factory
========================

In the root of our application package, let's create a new file called
``security.py`` with the following content.

.. literalinclude:: src/authorization/security.py
    :language: python
    :linenos:

This is the object that was mentioned a moment ago, a *context factory*.  It's
*not* tied to any specific entity in a database, and it returns an ``__acl__``
property which says that everyone has a ``'view'`` permission, and users that
are logged in also have ``'create'`` and ``'edit'`` permissions.


Create authentication and authorization policies
================================================

Now it's time to tell Pyramid about the policies we want to register with our
application.

Let's open our configuration ``__init__.py`` at the root of our project, and
add the following imports as indicated by the emphasized lines.

.. literalinclude:: src/authorization/__init__.py
    :language: python
    :linenos:
    :lines: 1-3
    :lineno-start: 1
    :emphasize-lines: 2-3

Now it's time to update our configuration.  We need to create our policies, and
pass them to the configurator.  Add or edit the emphasized lines.

.. literalinclude:: src/authorization/__init__.py
    :language: python
    :linenos:
    :lines: 8-14
    :lineno-start: 8
    :emphasize-lines: 1-5

The string "somesecret" passed into the policy will be a secret string used for
cookie signing, so that our authentication cookie is secure.

The last thing we need to add is to assign our context factory to our routes.
We want this to be the route responsible for entry creation and updates.
Modify the following emphasized lines.

.. literalinclude:: src/authorization/routes.py
    :language: python
    :linenos:
    :lines: 1-
    :lineno-start: 1
    :emphasize-lines: 5-6

Now for the finishing touch.  We set "create" and "edit" permissions on our
views.  Open ``views/blog.py``, and change our ``@view_config`` decorators as
shown by the following emphasized lines.

.. literalinclude:: src/authorization/views/blog.py
    :language: python
    :linenos:
    :lines: 18-20
    :lineno-start: 18
    :emphasize-lines: 2-3

.. literalinclude:: src/authorization/views/blog.py
    :language: python
    :linenos:
    :lines: 31-33
    :lineno-start: 31
    :emphasize-lines: 2-3


Current state of our application
================================

For convenience here are the two files you have edited in their entirety up to
this point (``security.py`` was already rendered above).


``__init__.py``
---------------

.. literalinclude:: src/authorization/__init__.py
    :language: python
    :linenos:
    :emphasize-lines: 2-3,18-24,29-30


``views/blog.py``
-----------------

.. literalinclude:: src/authorization/views/blog.py
    :language: python
    :linenos:
    :emphasize-lines: 18-20,31-33

Now if you try to visit the links to create or update entries, you will see
that they respond with a 403 HTTP status because Pyramid detects that there is
no user object that has ``edit`` or ``create`` permissions.

**Our views are secured!**

Next: :doc:`authentication`.
