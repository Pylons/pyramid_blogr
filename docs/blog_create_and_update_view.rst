==================================
6. Adding and editing blog entries
==================================

Form handling with WTForms library
----------------------------------

For form validation and creation, we will use a very friendly and easy to use
form library called WTForms. First we need to define our form schemas that will
be used to generate form HTML and validate values of form fields.

In the root of our application, let's create the file ``forms.py`` with
following content.

.. literalinclude:: src/blog_create_and_update_view/forms.py
    :language: python
    :linenos:

We create a simple filter that will be used to remove all the whitespace from
the beginning and end of our input.

Then we create a ``BlogCreateForm`` class that defines two fields:

* ``title`` has a label of "Title" and a single validator that will check the
  length of our trimmed data.  The title length needs to be in the range of
  1-255 characters.

* ``body`` has a label of "Contents" and a validator that requires its length
  to be at least 1 character.

Next is the ``BlogUpdateForm`` class that inherits all the fields from
``BlogCreateForm``, and adds a new hidden field called ``id``.  ``id`` will be
used to determine which entry we want to update.


Create blog entry view
----------------------

Now that our simple form definition is ready, we can actually write our view
code.

Lets start by importing our freshly created form schemas to ``views/blog.py``.

.. literalinclude:: src/blog_create_and_update_view/views/blog.py
    :language: python
    :linenos:
    :lines: 4-5
    :lineno-start: 4
    :emphasize-lines: 2

Add the emphasized line as indicated.

Next we implement a view callable that will handle new entries for us.

.. literalinclude:: src/blog_create_and_update_view/views/blog.py
    :language: python
    :linenos:
    :lines: 17-26
    :lineno-start: 17
    :emphasize-lines: 4-10

Only the emphasized lines need to be added or edited.

The view callable does the following:

* Create a new fresh entry row and form object from ``BlogCreateForm``.
* The form will be populated via POST, if present.
* If the request method is POST, the form gets validated.
* If the form is valid, our form sets its values to the model instance, and
  adds it to the database session.
* Redirect to the index page.

If the form doesn't validate correctly, the view result is returned, and a
standard HTML response is returned instead.  The form markup will have error
messages included.


Create update entry view
------------------------

The following view will handle updates to existing blog entries.

.. literalinclude:: src/blog_create_and_update_view/views/blog.py
    :language: python
    :linenos:
    :lines: 29-
    :lineno-start: 29
    :emphasize-lines: 4-13

Only the emphasized lines need to be added or edited.

Here's what the view does:

* Fetch the blog entry from the database based in the ``id`` query parameter.
* Show a 404 Not Found page if the requested record is not present.
* Create the form object, populating it from the POST parameters or from the
  actual blog entry, if we haven't POSTed any values yet.

.. note ::

  This approach ensures our form is always populated with the latest data from
  the database, or if the submission is not valid then the values we POSTed in
  our last request will populate the form fields.

* If the form is valid, our form sets its values to the model instance.
* Redirect to the blog page.

For convenience, here is the complete ``views/blog.py`` thusfar, with added and
edited lines emphasized.

.. literalinclude:: src/blog_create_and_update_view/views/blog.py
    :language: python
    :linenos:
    :emphasize-lines: 6,20-26,31-40



Create a template for creating and editing blog entries
-------------------------------------------------------

The final step is to add a template that will present users with the form to
create and edit entries.  Let's call it ``templates/edit_blog.jinja2`` and
place the following code as its content.

.. literalinclude:: src/blog_create_and_update_view/templates/edit_blog.jinja2
    :language: jinja
    :linenos:

Our template knows if we are creating a new row or updating an existing one
based on the ``action`` variable value.  If we are editing an existing row, the
template will add a hidden field named ``id`` that holds the id of the entry
that is being updated.

If the form doesn't validate, then the field errors properties will contain
lists of errors for us to present to the user.

Now launch the app, and visit http://localhost:6543/ and you will notice that
you can now create and edit blog entries.

.. note::

    Because WTForms form instances are iterable, you can easily write a
    template function that will iterate over its fields and auto generate
    dynamic HTML for each of them.

Now it is time to work towards securing them.

Next: :doc:`authorization`.
