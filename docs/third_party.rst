Third-party helpers
===================

The following third-party Python packages are not included in
WebHelpers2 due to their size or dependencies, but may be useful in
applications.

BeautifulSoup_

    A robust HTML/XML parser that can make sense of bad markup.

HTMLTidy_

    Clean up and pretty print HTML. This is a C library. There are several
    `Python bindings
    <http://pypi.python.org/pypi?%3Aaction=search&term=tidy&submit=search>`_ to
    it.

reprutils_

    Helpers to make a robust ``.__repr__`` method without reinventing
    the wheel.
    See also Python 3's ``dataclasses`` module.

Unidecode_

    Convert Unicode characters to ASCII equivalents. Accented letters and
    symbols are converted to a visual approximation, and non-Latin letters
    are converted to their standard Latin pronounciation.  Several of the
    ``convert_\*`` functions in ``webhelpers.text`` will use Unidecode if
    it's installed.

Unipath_

    An object-oriented alternative to the path functions in ``os``,
    ``os.path``, and ``shutil``.
    Python 3 now has a `pathlib` module with some of these features.


.. include:: include.rst
