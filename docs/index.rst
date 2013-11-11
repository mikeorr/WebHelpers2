WebHelpers2
%%%%%%%%%%%
:Version: |release|, released 2013-11-11
:PyPI: http://pypi.python.org/pypi/WebHelpers2
:Docs: https://webhelpers2.readthedocs.org/en/latest/
:Source: https://github.com/mikeorr/WebHelpers2 (Git)

.. image:: _static/webhelpers-logo.png
   :width: 100px
   :height: 100px
   :alt: WebHelpers Logo
   :align: right

**WebHelpers2** is the successor to the widely-used WebHelpers_ utility functions.
It narrows the focus to a core set of utilities that are most widely
used, relevant to Pyramid and other current frameworks, and easiest to maintain
and port to Python 3. In particular it keeps the HTML builder and HTML tag functions, and
most of the text-processing, number formatting, statistics, and date functions,
See :ref:`migrate` if you're currently using WebHelpers or an early WebHelpers2
beta.

**Version 2.0b4** finishes the API reorganization (except the 'html'
subpackage), adds a migration chapter to the documentation, and switches to
PyTest for unit testing.  The remaining work is to port the code to Python 3
(using 'six' if necessary), and refactor the 'html' submodule. This version is
tested on Python 2.7.4 and should work on 2.6. 

WebHelpers2 depends on MarkupSafe_, and can use Unidecode_ if it's installed.
An extensive test suite for PyTest is included.
For support/questions/patches, please use the pylons-discuss_ mailing list.

.. toctree::
   :maxdepth: 2

   contents

.. toctree::
   :maxdepth: 1

   migrate
   changelog
   third_party
   todo

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _MarkupSafe: http://pypi.python.org/pypi/MarkupSafe
.. _Unidecode: http://pypi.python.org/pypi/Unidecode/
.. _pylons-discuss: http://groups.google.com/group/pylons-discuss
.. _WebHelpers: http://pypi.python.org/pypi/WebHelpers
