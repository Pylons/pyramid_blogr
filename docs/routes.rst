=====================
3. Application routes
=====================

This is the point where we want to define our routes that will be used to map 
view callables to request paths. 

URL dispatch provides a simple way to map URLs to view code using a simple 
pattern matching language.

Our application will consist of few sections:

* index page that will list all of our sorted blog entries
* a sign in/sign out section that will be used for authentication
* a way to create and edit our blog posts

Our urls could look like this:

To sign in users::

    /sign/in

So when user visits http://somedomain.foo/sign/in - the view callable responsible 
for signing in the user based on POST vars will be executed.

To sign out users::
    
    /sign/out

Index page (it is already defined via default scaffold under name "home")::

    /

Creation of new blog entries::

    /blog/{action}
 
You probably noted that this url looks somewhat different, the {action} part in 
the pattern determines that this part is dynamic, so our URL could look like::

    /blog/create
    /blog/edit
    /blog/foobar
 
This single route could map to different views. 
 
Finally a route used to for our blog entries::

    /blog/{id:\d+}/{slug} 
    
This route constists of two dynamic parts, {id:\\d+} and {slug}.

The **:\d+** pattern means that the route will only match integers, so url like::

    /blog/156/Some-blog-entry
   
would work, but this one will not be matched::

    /blog/something/Some-blog-entry
    
Basics of pyramid configuration
-------------------------------

Now that we know what routes we want we should add them to our application.

Pyramid's config object will store them for us. To access it we will need to 
open the file __init__.py in root of our project. This is the central point that 
will perform initial application configuration on runtime.

The main function will accept parsed ini file that we passed to our pserve 
command.

Lets quickly go over what this file does by default.
::

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    
Those lines read the settings for SQLAlchemy and configure connection engine and 
session maker objects. ::

    config = Configurator(settings=settings)
    
This creates the configurator itself, when needed we will be able to access it 
in our views via request object as *request.registry.settings*.
::

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
Now two routes are added:

* **static route** that starts with */static* - that will serve all our 
  static files like javascript, css, images. When a browser makes a request to 
  */static/some/resource.foo*, our application will check if /some/resource.foo 
  resource is present in our static dir, if it's there it will get 
  served to browser. 
  
* **view route** called *"home"* that maps to path */*.

::

    config.scan()
    
This runs the scan process that will scan all our whole project and load all 
decorators and includes to add them to our config object.

::

    return config.make_wsgi_app()

Instance of WSGI app is returned to the server.

Adding routes to application configuration
------------------------------------------

Lets add our routes to configurator after "home" route::

    config.add_route('blog', '/blog/{id:\d+}/{slug}')
    config.add_route('blog_action', '/blog/{action}')
    config.add_route('auth', '/sign/{action}')
    
Now we are ready to develop actual views

Next  :doc:`initial_views`
