Installation and Testing
%%%%%%%%%%%%%%%%%%%%%%%%

Installing WebHelpers2
======================

Install WebHelpers2 from PyPI:

.. code-block:: sh

   $ pip install WebHelpers2

or check out the source:

.. code-block:: sh

   $ git clone https://github.com/mikeorr/WebHelpers2
   $ pip install .

It depends on MarkupSafe_ and six_, which pip will automatically
install. Unidecode_ is optional; some of the text helpers will use it if
it's installed.

To install all optional components and everything needed to run the
tests and build the documentation in one step, check out the source and
run:

.. code-block:: sh

   $ pip install -r requirements.txt

WebHelpers2 has been tested on Python 2.7 and 3.4. Earlier betas were
tested on Python 3.3 and it's believed to still be compatible.


Python 3.2 Caveats
==================

On Python 3.2 you'll have to use MarkupSafe_ 0.15. Version 0.16 started
using the "u" string prefix which is invalid in Python 3.0 - 3.2. (It was
re-added in 3.3.)

WebHelpers2 is believed to run on Python 3.2 but this has not yet been tested.
All "u" prefixes have been removed from the code but remain in some
former doctests.  (These are no longer supported as doctests but only as
documentation.)


Running the unit tests
======================

WebHelpers2 has an extensive test suite using PyTest. To run the tests:

.. code-block:: sh

   $ pip install pytest
   $ py.test

PyTest has lots of options. To run a specific test module, pass the
filename; e.g., 'webhelpers2/tests/test_text.py'.


.. include:: include.rst
