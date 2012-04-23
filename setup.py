import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'Jinja2',
    'path.py',
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid-jinja2',
    'waitress',
    'requests',
    'simplejson',
    'redis'
    ]

setup(name='Doula',
      version='0.0',
      description='Doula',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="doula",
      entry_points = """\
      [paste.app_factory]
      main = doula:main
      """,
      )

