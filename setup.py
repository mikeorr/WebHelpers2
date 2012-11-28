try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from webhelpers import __version__

setup(
    name="WebHelpers",
    version=__version__,
    description='Web Helpers',
    long_description="""
Web Helpers is a library of helper functions intended to make writing 
web applications easier. It's the standard function library for
Pylons and TurboGears 2, but can be used with any web framework.  It also
contains a large number of functions not specific to the web, including text
processing, number formatting, date calculations, container objects, etc.

Version 1.3 fixes a performance regression in 1.2 regarding paginate with
SQLAlchemy.

WebHelpers itself depends only on MarkupSafe, but certain helpers depend on
third-party packages as described in the docs.

The development version of WebHelpers is at
http://bitbucket.org/bbangert/webhelpers (Mercurial)

""",
    author='Mike Orr, Ben Bangert, Phil Jenvey',
    author_email='sluggoster@gmail.com, ben@groovie.org, pjenvey@groovie.org',
    url='http://webhelpers.groovie.org/',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'MarkupSafe>=0.9.2',
        ],
    tests_require=[ 
      'Nose',
      'Routes',
      'WebOb',
      ], 
    test_suite='nose.collector',
    classifiers=["Development Status :: 4 - Beta",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: BSD License",
                 "Programming Language :: Python",
                 "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
                 "Topic :: Software Development :: Libraries :: Python Modules",
               ],
    entry_points="""
    [buildutils.optional_commands]
    compress_resources = webhelpers.commands
    """,
)
