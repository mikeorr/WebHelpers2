try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys
from webhelpers2 import __version__

requires = [
    'MarkupSafe>=0.9.2',
    ]

if sys.version_info < (2, 7):
    requires.append('ordereddict')

setup(
    name="WebHelpers2",
    version=__version__,
    description='WebHelpers2',
    long_description="""
WebHelpers2 is the successor to the widely-used WebHelpers utilities.
It contains convenience functions to make HTML tags, process text, format numbers, do basic statistics, work with collections, and more.
""",
    author='Mike Orr, Ben Bangert, Phil Jenvey',
    author_email='sluggoster@gmail.com, ben@groovie.org, pjenvey@groovie.org',
    url='https://webhelpers2.readthedocs.org/en/latest/',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    include_package_data=True,
    install_requires=requires,
    tests_require=[ 
      'Nose',
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
    """,
)
