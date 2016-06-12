.. _blogr_requirements:

============
Requirements
============

.. note::

  This section was modified from the original :ref:`Pyramid Quick Tutorial
  Requirements <pyramid:qtut_requirements>`.

Let's get our tutorial environment setup. Most of the setup work is in standard
Python development practices (install Python, make an isolated environment, and
setup packaging tools.)

.. note::

  Pyramid encourages standard Python development practices with packaging
  tools, virtual environments, logging, and so on.  There are many variations,
  implementations, and opinions across the Python community.  For consistency,
  ease of documentation maintenance, and to minimize confusion, the Pyramid
  *documentation* has adopted specific conventions.

This *Pyramid Blogr Tutorial* is based on:

* **Python 3.3**. Pyramid fully supports Python 3.2+ and Python 2.6+. This
  tutorial uses **Python 3.3** but runs fine under Python 2.7.

* **pyvenv**. We believe in virtual environments. For this tutorial, we use
  Python 3's built-in solution, the ``pyvenv`` command. For Python 2.7, you can
  install ``virtualenv``.

* **pip**. We use ``pip`` for package management.

* **Workspaces, projects, and packages**. Our home directory will contain a
  *tutorial workspace* with our Python virtual environment(s) and *Python
  projects* (a directory with packaging information and *Python packages* of
  working code.)

* **UNIX commands**. Commands in this tutorial use UNIX syntax and paths.
  Windows users should adjust commands accordingly.

.. note::

  Pyramid was one of the first web frameworks to fully support Python 3 in
  October 2011.


Steps
=====

#. :ref:`install-python-3.3-or-greater`
#. :ref:`workspace-and-project-directory-structure`
#. :ref:`set-an-environment-variable`
#. :ref:`create-a-virtual-environment`
#. :ref:`install-pyramid`


.. _install-python-3.3-or-greater:

Install Python 3.3 or greater
-----------------------------

Download the latest standard Python 3.3+ release (not development release) from
`python.org <https://www.python.org/downloads/>`_.

Windows and Mac OS X users can download and run an installer.

Windows users should also install the `Python for Windows extensions
<http://sourceforge.net/projects/pywin32/files/pywin32/>`_. Carefully read the
``README.txt`` file at the end of the list of builds, and follow its
directions. Make sure you get the proper 32- or 64-bit build and Python
version.

Linux users can either use their package manager to install Python 3.3+ or may
`build Python 3.3+ from source
<http://pyramid.readthedocs.org/en/master/narr/install.html#package-manager-
method>`_.


.. _workspace-and-project-directory-structure:

Workspace and project directory structure
-----------------------------------------

We will arrive at a directory structure of ``workspace -> project -> package``,
with our workspace named ``blogr_tutorial``. The following tree diagram shows
how this will be structured and where our virtual environment will reside as we
proceed through the tutorial:

.. code-block:: text

    ~/
    └── projects/
        └── blogr_tutorial/
            ├── env/
            └── pyramid_blogr/
                ├── CHANGES.txt
                ├── MANIFEST.in
                ├── README.txt
                ├── development.ini
                ├── production.ini
                ├── pytest.ini
                ├── pyramid_blogr/
                │   ├── __init__.py
                │   ├── models
                │   │   ├── __init__.py
                │   │   ├── meta.py
                │   │   └── mymodel.py
                │   ├── routes.py
                │   ├── scripts/
                │   │   ├── __init__.py
                │   │   └── initializedb.py
                │   ├── static/
                │   │   ├── pyramid-16x16.png
                │   │   ├── pyramid.png
                │   │   └── theme.css
                │   ├── templates/
                │   │   ├── 404.jinja2
                │   │   ├── layout.jinja2
                │   │   └── mytemplate.jinja2
                │   ├── tests.py
                │   └── views
                │   │   ├── __init__.py
                │   │   ├── default.py
                │   │   └── notfound.py
                └── setup.py

For Linux, the commands to do so are as follows:

.. code-block:: bash

    # Mac and Linux
    $ cd ~
    $ mkdir -p projects/blogr_tutorial
    $ cd projects/blogr_tutorial

For Windows:

.. code-block:: bash

    # Windows
    c:\> cd \
    c:\> mkdir projects\blogr_tutorial
    c:\> cd projects\blogr_tutorial

In the above figure, your user home directory is represented by ``~``.  In your
home directory, all of your projects are in the ``projects`` directory. This is
a general convention not specific to Pyramid that many developers use. Windows
users will do well to use ``c:\`` as the location for ``projects`` in order to
avoid spaces in any of the path names.

Next within ``projects`` is your workspace directory, here named
``blogr_tutorial``. A workspace is a common term used by integrated development
environments (IDE) like PyCharm and PyDev that stores isolated Python
environments (virtualenvs) and specific project files and repositories.


.. _set-an-environment-variable:

Set an environment variable
---------------------------

This tutorial will refer frequently to the location of the virtual environment.
We set an environment variable to save typing later.

.. code-block:: bash

    # Mac and Linux
    $ export VENV=~/projects/blogr_tutorial/env

    # Windows
    # TODO: This command does not work
    c:\> set VENV=c:\projects\blogr_tutorial\env


.. _create-a-virtual-environment:

Create a virtual environment
----------------------------

.. warning::

  The current state of isolated Python environments using ``pyvenv`` on Windows
  is suboptimal in comparison to Mac and Linux.  See
  http://stackoverflow.com/q/15981111/95735 for a discussion of the issue and
  `PEP 453 <http://www.python.org/dev/peps/pep-0453/>`_ for a proposed
  resolution.

``pyvenv`` is a tool to create isolated Python 3 environments, each with its
own Python binary and independent set of installed Python packages in its site
directories. Let's create one, using the location we just specified in the
environment variable.

.. code-block:: bash

    # Mac and Linux
    $ pyvenv $VENV

    # Windows
    c:\> c:\Python33\python -m venv %VENV%

.. seealso::

  See also Python 3's :mod:`venv module <python3:venv>`.
  For instructions to set up your Python environment for development on UNIX or
  Windows, or using Python 2, see Pyramid's :ref:`Before You Install
  <pyramid:installing_chapter>`.


.. _install-pyramid:

Install Pyramid
---------------

We have our Python standard prerequisites out of the way. The Pyramid part is
pretty easy:

.. TODO
  whenever this gets merged into the official Pyramid docs, uncomment the
  following parsed-literal block and delete the subsequent code-block.

.. .. parsed-literal::
    # Mac and Linux
    $ $VENV/bin/pip "pyramid==\ |release|\ "


..  # Windows
    c:\\> %VENV%\\Scripts\\pip "pyramid==\ |release|\ "


.. code-block:: bash

    # Mac and Linux
    $ $VENV/bin/pip install pyramid==1.7

    # Windows
    c:\> %VENV%\Scripts\pip install pyramid==1.7

Our Python virtual environment now has the Pyramid software available.

With the requirements satisfied, you may continue to the next step in this
tutorial :doc:`project_structure`.
