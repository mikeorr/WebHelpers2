import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand

from webhelpers2 import __version__

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


install_requires=[
    "MarkupSafe>=0.9.2",
    "six>=1.4.0",
    ],

setup(
    name="WebHelpers2",
    version=__version__,
    description='WebHelpers2',
    long_description="""
**WebHelpers2** contains convenience functions to make HTML tags, process text,
format numbers, do basic statistics, work with collections, and more.
It's the successor to WebHelpers.

Version 2.1 fixes bugs and adds Python 3 support. The API and features are
unchanged since 2.0. This version is tested on Python 3.9, 3.10, 3.11, 3.12,
and 2.7.

The next version will drop Python 2 and older Python 3 versions. No new
helpers or API changes are expected. It will focus on updating the packaging
and documentation. It may delete some helpers that now have equivalents in
recent Python versions.

For support/questions/patches, please use the pylons-discuss_ mailing list.

.. _pylons-discuss: http://groups.google.com/group/pylons-discuss
""",
    author='Mike Orr, Ben Bangert, Phil Jenvey',
    author_email='sluggoster@gmail.com, ben@groovie.org, pjenvey@groovie.org',
    url='https://webhelpers2.readthedocs.org/en/latest/',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    tests_require=[ 
      'pytest',
      ], 
    cmdclass = {'test': PyTest},
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Environment :: Web Environment",
                 "Framework :: Pylons",
                 "Framework :: Pyramid",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Programming Language :: Python",
                 "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
                 "Topic :: Software Development :: Libraries :: Python Modules",
               ],
    entry_points="""
    """,
)
