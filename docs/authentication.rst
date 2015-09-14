=================
8. Authentication
=================

Great, we secured our views, but now no one can add new entries to our 
application, so the finishing touch is to implement our authentication views.

First we need to add a login form to our existing **index.mako** template::

    <%inherit file="pyramid_blogr:templates/layout.mako"/>

    ...

    % if request.authenticated_userid:
        Welcome <strong>${request.authenticated_userid}</strong> ::
        <a href="${request.route_url('auth',action='out')}">Sign Out</a>
    %else:
        <form action="${request.route_url('auth',action='in')}" method="post" class="form-inline">
            <div class="form-group">
                <label>User</label> <input type="text" name="username" class="form-control">
            </div>
            <div class="form-group">
            <label>Password</label> <input type="password" name="password" class="form-control">
            <input type="submit" value="Sign in" class="btn btn-default">
            </div>
        </form>
    %endif
    
    % if paginator.items:
        ...

Now the template first check if we are logged in, if we are it greets the user, 
and presents sign-out link. Otherwise we are presented with sign-in form.

Now it's time to update our views and User model.

Lets update our model with two methods, "verify_password" to check user input 
with password associated with user instance and "by_name" that will fetch 
our user from database based on login.

We add following method to our User class in models.py::

    def verify_password(self, password):
        return self.password == password

We also need to create UserService class in models/services/user.py::

    from ..meta import DBSession
    from ..user import User

    class UserService(object):

        @classmethod
        def by_name(cls, name):
            return DBSession.query(User).filter(User.name == name).first()

.. warning::
    In a real application verify_password should be using some strong way 
    one-way hashing algorithm like bcrypt or pbkdf2. Use a package like 
    **cryptacular** to provide strong hashing.

The final step is to update the view that handles authentication.

First we need to add following import to views/default.py::

    from pyramid.httpexceptions import HTTPFound
    from pyramid.security import remember, forget
    from ..models.services.user import UserService

Those functions will return headers used to set our AuthTkt cookie 
(from AuthTktAuthenticationPolicy) for users browser, "remember" is used to 
set the current user, "forget" is used to sign out our users.

Now we have everything ready to implement our actual view::

    @view_config(route_name='auth', match_param='action=in', renderer='string',
                 request_method='POST')
    @view_config(route_name='auth', match_param='action=out', renderer='string')
    def sign_in_out(request):
        username = request.POST.get('username')
        if username:
            user = UserService.by_name(username)
            if user and user.verify_password(request.POST.get('password')):
                headers = remember(request, user.name)
            else:
                headers = forget(request)
        else:
            headers = forget(request)
        return HTTPFound(location=request.route_url('home'),
                         headers=headers)

This is a very simple view that checks if database row with name supplied by 
user is present is in database, if it is a password check is performed.
If password check was successful a new set of headers used to set the cookie is 
generated and passed back to the client on redirect.
If user is not found or password doesnt match a set of headers meant to remove 
the cookie (if any) is issued.

**Voilà!!!** 

Congratulations, this tutorial is now complete, you can now sign in and out to 
add/edit blog entries using login `admin` with password `admin` (this user was added to database during `initialize_db step`).

Now is the time to go back to documentation to read on the details of 
functions/packages used in this example. I've barely scratched the surface of 
what is possible with Pyramid.

.. toctree::

   authentication_src
