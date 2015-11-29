import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid==1.5.7',
    'pyramid_jinja2', # replaces default chameleon templates
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy==1.0.8',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'wtforms==2.0.2',  # form library
    'webhelpers2==2.0', # various web building related helpers
    'paginate==0.5', # pagination helpers
    'paginate_sqlalchemy==0.2.0',
    'passlib'
]

docs_extras = [
    'Sphinx >= 1.3.1', # Read The Docs minimum version
    'docutils',
    'repoze.sphinx.autointerface',
    'pylons-sphinx-themes',
]

setup(name='pyramid_blogr',
      version='0.0',
      description='pyramid_blogr',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pyramid_blogr',
      install_requires=requires,
      extras_require = {
          'docs':docs_extras,
      },
      entry_points="""\
      [paste.app_factory]
      main = pyramid_blogr:main
      [console_scripts]
      initialize_pyramid_blogr_db = pyramid_blogr.scripts.initializedb:main
      """,
      )
