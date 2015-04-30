================
7. Authorization
================

At this point we have a fully working application but you have probably noticed 
everyone can alter our entries. We should change that by introducing user 
authentication and permission checks.

For the sake of simplicity of this tutorial we will assume that every user can 
edit every blog entry as long as he/she is signed in to our application.

Pyramid provides some ready-made policies for this and mechanisms for writing 
custom ones aswell.

We will use the ones provided with framework:

* **AuthTktAuthenticationPolicy**

  Obtains user data from a Pyramid “auth ticket” cookie.
  
* **ACLAuthorizationPolicy**

  An authorization policy which consults an ACL object attached to a context to 
  determine authorization information about a principal or multiple principals.

OK, so **ACLAuthorizationPolicy** explanation has a lots of scary words in it, 
but in practice it's a simple concept that allows for great flexibility when 
defining permission systems.

The policy basicly checks if user has a permission to specific context of a view 
based on Access Control Lists.

**What does this mean, what is a context?**

A context could be anything, imagine you are building a forum application, 
and you want to add a functionality where only moderators will be able to edit 
specific topic of a specific forum. - in this case our context would be forum 
object - it would have attached info about who has specific permissions to this 
resource.

Or something simplier, who can access admin page? In this case a context would 
be an arbitrary object that has information attached about who is administrator 
of the site.

**How does this relate to our application?**

Since our application does not track who owns blog entries, we will also assume 
the latter scenario. We will make the most trivial context factory object - as 
its name implies factory will return the context object (in our class an 
arbitrary class).

It will say that *everyone logged* to our application can create and edit, 
blog entries.

In root of our application package lets create a new file called security.py 
with following contents ::

    from pyramid.security import Allow, Everyone, Authenticated

    class EntryFactory(object):
        __acl__ = [(Allow, Everyone, 'view'),
                   (Allow, Authenticated, 'create'),
                   (Allow, Authenticated, 'edit'), ]
        
        def __init__(self, request):
            pass

This is the object that was mentioned a moment ago (It's called context factory), 
it's **not** tied to any specific entity in a database, and returns __acl__ 
property that says that everyone has a *'view'* permission and users that are 
logged in also have *create* and *edit* permissions.

Now it's time to tell pyramid about what policies we want to register with our 
app.


Let's open our configuration related __init__.py and add following imports::

    from pyramid.authentication import AuthTktAuthenticationPolicy
    from pyramid.authorization import ACLAuthorizationPolicy
    from .security import EntryFactory

Now it's time to update our configuration, we need to create our policies, and 
pass them to configurator::

    authentication_policy = AuthTktAuthenticationPolicy('somesecret', hashalg='sha512')
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy
                          )

"somesecret" passed to policy will be a secret string used for cookie signing, 
so our auth cookie is secure.

The last thing we need to add is to assign our context factory to our routes, 
we want this to be the route responsible for entry creation/updates::

    config.add_route('blog_action', '/blog/{action}',
                     factory='pyramid_blogr.security.EntryFactory')

Now the finishing touch, we set "create" and "edit" permissions on our views.

For this we need to change our view_config decorators like this::

    @view_config(route_name='blog_action', match_param='action=create',
                 renderer='pyramid_blogr:templates/edit_blog.mako',
                 permission='create')
                 ...
                 
    @view_config(route_name='blog_action', match_param='action=edit',
                 renderer='pyramid_blogr:templates/edit_blog.mako',
                 permission='edit')
                 ...
             
Now if you try to visit the links to create/update entries you will see that 
they actually respond with 403 HTTP status.

**Our views are secured!**

.. toctree::

   authorization_src
