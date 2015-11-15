.. _blogr_registration:

===============
9. Registration
===============

Now we have a basic functioning application, but we have only one user hardcoded administrator that can add blogs.
We can provide a registration page for our users to sign in to.

Then we need to to provide a quality hashing solution so we can store secure password hashes instead of cleartextm
this functionality will be provided by **passlib**.


We should create a form to handle registration requests, lets open `forms.py` and add a new form class::

   # add missing PasswordField at the top of the file

   class RegistrationForm(Form):
       username = StringField('Username', [validators.Length(min=1, max=255)],
                              filters=[strip_filter])
       password = PasswordField('Password', [validators.Length(min=3)])


Our second step will be adding a new route that handles user registration in our main `__init__.py` file::

    ...
    config.add_route('auth', '/sign/{action}')
    config.add_route('register', '/register')
    config.scan()
    ...

We should add link to the registration page in our `index.jinja2` template so we can easly navigate to it::

    % if request.authenticated_userid:
        Welcome <strong>${request.authenticated_userid}</strong> ::
        <a href="${request.route_url('auth',action='out')}">Sign Out</a>
    %else:
        <form action="${request.route_url('auth',action='in')}" method="post" class="form-inline">
         ...
        </form>
        <a href="{{request.route_url('register')}}">Register here</a>
    %endif

So at this point we have the form object and routing set up, we are missing related view, model and template code.
Let us move forward with the view code in `views/default.py`.

First we need to import our form definition user model at the top of the file::

    ...
    from ..forms import RegistrationForm
    from ..models.meta import DBSession
    from ..models.user import User
    ...

And we can start implementing our view logic::

    @view_config(route_name='register', renderer='pyramid_blogr:templates/register.jinja2')
    def register(request):
        form = RegistrationForm(request.POST)
        if request.method == 'POST' and form.validate():
            new_user = User()
            new_user.username = form.username.data
            new_user.password = form.password.data
            DBSession.add(new_user)
            return HTTPFound(location=request.route_url('home'))
        return {'form': form}

Next, let us start by creating a new registration template called `register.jinja2` with following contents::

    {% extends "pyramid_blogr:templates/layout.jinja2" %}

    {% block content %}
    <h1>Register</h1>

    <form action="{{request.route_url('register')}}" method="post" class="form">

        {% for error in form.username.errors %}
        <div class="error">{{ error }}</div>
        {% endfor %}

        <div class="form-group">
            <label for="title">{{form.username.label}}</label>
            {{form.username(class_='form-control')}}
        </div>

        {% for error in form.password.errors %}
        <div class="error">{{error}}</div>
        {% endfor %}

        <div class="form-group">
            <label for="body">{{form.password.label}}</label>
            {{form.password(class_='form-control')}}
        </div>
        <div class="form-group">
            <label></label>
            <button type="submit" class="btn btn-default">Submit</button>
        </div>


    </form>
    <p><a href="{{request.route_url('home')}}">Go Back</a></p>
    {% endblock %}

Our users can now register themselves and are stored within database using unencrypted passwords (which is
a really bad idea).

This is exactly where **passlib** comes into play, so we should add it to our projects requirements in `setup.py`::

    requires = [
        ...
        'paginate==0.5', # pagination helpers
        'paginate_sqlalchemy==0.2.0',
        'passlib'
    ]

Now we can run `pip install passlib` or run `python setup.py develop` to pull in new dependency to our project -
password hashing will be implemented in our `User` model class.

We need to import the hash context object from passlib and alter `User` class to contain new versions of methods
`verify_password` and `set_password`, our file should look like this::

    from passlib.apps import custom_app_context as blogger_pwd_context

    class User(Base):
        __tablename__ = 'users'

        ...

        def verify_password(self, password):
            return blogger_pwd_context.verify(password, self.password)

        def set_password(self, password):
            password_hash = blogger_pwd_context.encrypt(password)
            self.password = password_hash

The last step is to alter our `views/default.py` to set password like this::

        ...
        new_user.name = form.username.data
        new_user.set_password(form.password.data.encode('utf8'))
        DBSession.add(new_user)
        ...


Now our passwords are properly hashed and can be securely stored.

If you tried to log in with `admin/admin` credentials you may notice that the application threw exception
`ValueError: hash could not be identified` because our old clear text passwords are not identified,
so we should allow our application to migrate to secure hashes (usually strong sha512_crypt if we are using the
quickstart class).

We can easly fix this by altering our `verify_password` method::

    def verify_password(self, password):
        # is it cleartext?
        if password == self.password:
            self.set_password(password)

        return blogger_pwd_context.verify(password, self.password)

Keep in mind that for proper migration of valid hash schemes passlib provides
mechanism you can use to quickly upgrade from one scheme to another.

