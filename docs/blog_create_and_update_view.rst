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

Create blog entry view
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

Create update entry view
------------------------

The following view will handle updates to existing blog entries::

    @view_config(route_name='blog_action', match_param="action=edit",
                 renderer="pyramid_blogr:templates/edit_blog.mako")
    def blog_update(request):
        id = int(request.params.get('id', -1))
        entry = Entry.by_id(id)
        if not entry:
            return HTTPNotFound()
        form = BlogUpdateForm(request.POST, entry)
        if request.method == 'POST' and form.validate():
            form.populate_obj(entry)
            return HTTPFound(location=request.route_url('blog', id=entry.id,
                                                        slug=entry.slug))
        return {'form':form, 'action':request.matchdict.get('action')}

What it does step by step:

* we fetch blog entry from the database based on the "id" query parameter
* we show 404 page if its hot present
* the form object is created, it gets populated from POST, and actual entry 
  if we haven't POST-ed any values yet.
  
.. hint ::
  This approach ensures our form is always populated with latest data from 
  database, OR if it's not validated - with values we posted in our last request.
   
* if the form is valid - our form sets its values to the model instance
* redirect to blog page is performed

The final step is to add a view that will present users with form to create and 
edit entries, lets call it *edit_blog.mako* ::

    <%inherit file="pyramid_blogr:templates/layout.mako"/>
    
    <form action="${request.route_url('blog_action',action=action)}" method="post">
    %if action =='edit':
    ${form.id()}
    %endif
    
    % for error in form.title.errors:
        <div class="error">${ error }</div>
    % endfor
    
    <div><label>${form.title.label}</label>${form.title()}</div>
    
    % for error in form.body.errors:
    <div class="error">${error}</div>
    % endfor
    
    <div><label>${form.body.label}</label>${form.body()}</div>
    <div><input type="submit" value="Submit"></div>
    </form>
    <p><a href="${request.route_url('home')}">Go Back</a></p>
    
    <style type="text/css">
    form{
        text-align: right;
    }
    label{
        min-width: 150px;
        vertical-align: top;
        text-align: right;
        display: inline-block;
    }
    input[type=text]{
        min-width: 505px;
    }
    textarea{
        color: #222;
        border: 1px solid #CCC;
        font-family: sans-serif;
        font-size: 12px;
        line-height: 16px;
        min-width: 505px;
        min-height: 100px; 
    }
    .error{
        font-weight: bold;
        color: red;
    }
    </style>

Our template knows if we are creating new row or updating existing one based on 
action variable value, if we are editing existing row - it will add a hidden 
field "id" that holds the id of entry that is being updated. 

If the form doesn't validate field errors properties contain lists of errors for 
us to present to user.

.. hint::
    Because WTForms form instances are iterable you can easly write a template, 
    function that will iterate over their fields and auto generate dynamic html 
    for each of them.  


.. toctree::

   blog_create_and_update_view_src.rst