==================================
6. Adding and editing blog entries
==================================

Form handling with WTForms library
----------------------------------

For form validation and creation we will use a very friendly and easy to use 
form library called WTForms. First, we need to define our form schemas, that 
will be used to generate form HTML and validation of form fields.  

First in root of our application lets create file *forms.py* with following 
contents::

    from wtforms import Form, BooleanField, TextField, TextAreaField, validators
    from wtforms import HiddenField
    
    strip_filter = lambda x: x.strip() if x else None
    
    class BlogCreateForm(Form):
        title = TextField('Entry title', [validators.Length(min=1, max=255)],
                          filters=[strip_filter])
        body = TextAreaField('Entry body', [validators.Length(min=1)],
                             filters=[strip_filter])
        
    class BlogUpdateForm(BlogCreateForm):
        id = HiddenField()

    
We create a simple filter that will be used to remove all the whitespace 
from the beginning and end of our input.

Then we create a BlogCreateForm class that defines 2 fields:

* **title** - it has a label of "Title" and single validator that will check the 
  length of our trimmed data - the title length needs to be between 1-255 
  characters.
  
* **body** has a label of "Contents", also has a validator that requires its 
  length to be at least 1 character.

Next is BlogUpdateForm class that inherits all the fields from BlogCreateForm, 
and adds a new hidden field called id - it will be used to determine which 
entry we want to update.

Create and update view
----------------------

Now that our simple form definition is ready we can actually write our view code.

Lets start by importing our freshly created form schemas to views.py::

    from .forms import BlogCreateForm, BlogUpdateForm

Next we implement actual view callable that will handle new entries for us::

    @view_config(route_name='blog_action', match_param="action=create",
                 renderer="pyramid_blogr:templates/edit_blog.mako")
    def blog_create(request): 
        entry = Entry()
        form = BlogCreateForm(request.POST)
        if request.method == 'POST' and form.validate():
            form.populate_obj(entry)
            DBSession.add(entry)
            return HTTPFound(location=request.route_url('home'))
        return {'form':form, 'action':request.matchdict.get('action')}

What it does step by step:

* we create a new fresh entry row and form object from BlogCreateForm
* the form will be populated via POST if present
* if request method is POST the form gets validated
* if the form is valid - our form sets its values to the model instance, 
  and adds it to the database session
* redirect to index page is performed

If the form doesn't validate correctly, view result is returned and standard 
HTML response is returned instead - form markup will have error messages included.


.. toctree::

   blog_create_and_update_view_src.rst