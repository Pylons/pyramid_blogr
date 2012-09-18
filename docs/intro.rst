=================================================
What you will know after you finish this tutorial
=================================================

The tutorial is really simple but should be enough of a head start to writing 
applications using Pyramid Web Framework. By the end of it you should have a 
basic understanding of templating, working with databases, using url routes to 
launch our business logic(views) and authentication, example of form library 
usage and pagination of our blog entries.

Pyramid_flaskr makes some initial assumptions:

* Will use **alchemy** scaffold with SQLAlchemy as it's ORM layer
* **Mako** templates will be our choice for templating engine
* **URL dispatch** will be the default way for our view resolution
* A single user in database will be created in setup phase
* Will perform a simple authentication of the user
* Authenticated user will be able to make blog entries
* The entries will be listed from newest to oldest one
* We will use **webhelpers** package for pagination
* **WTForms** form library will provide form validation