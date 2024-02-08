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
   $ python -m pip install .

It depends on MarkupSafe_ and six_, which pip will automatically
install. Unidecode_ is optional; some of the text helpers will use it if
it's installed.

To install all optional components and everything needed to run the
tests and build the documentation in one step, check out the source and
run:

.. code-block:: sh

   $ pip install -r requirements.txt


Running the unit tests
======================

WebHelpers2 has an extensive test suite using PyTest. To run the tests,
check out the source and run:

.. code-block:: sh

   $ python -m pip install pytest
   $ py.test tests

PyTest has lots of options. To run a specific test module, pass the
filename; e.g., 'tests/test_text.py'.


.. include:: include.rst
