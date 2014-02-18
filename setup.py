import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'wtforms',
    'webhelpers2==2.0b5',
    'paginate'
    ]

setup(name='pyramid_blogr',
      version='0.0',
      description='pyramid_blogr',
      long_description=README + '\n\n' +  CHANGES,
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
      entry_points="""\
      [paste.app_factory]
      main = pyramid_blogr:main
      [console_scripts]
      initialize_pyramid_blogr_db = pyramid_blogr.scripts.initializedb:main
      """,
      )

