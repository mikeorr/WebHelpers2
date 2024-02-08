WebHelpers2
++++++++++++

**WebHelpers2** contains convenience functions and classes to make HTML tags,
process text, format numbers, do basic statistics, work with collections, and
more. It's the successor to WebHelpers.

**Version 2.1** fixes bugs and adds Python 3 support. The API and features are
unchanged since 2.0. This version works on both Python 3 and 2. It was tested
on Python 3.9, 3,10, 3,11, 3.12, and 2.7 on Linux, and should work on other platforms.

**The next version** will drop Python 2 and older Python 3 versions.
No new helpers or API changes are expected.
Instead it will focus on updating the packaging and documentation.
It may delete some helpers that now have equivalents in recent Python versions.

For support/questions/patches, please use the pylons-discuss_ mailing list.

WebHelpers2 contains convenience functions to make HTML tags, process text,
format numbers, do basic statistics, work with collections, and more.
It's the successor to WebHelpers.

Version 2.1 fixes bugs and adds Python 3 support. The API and features are
unchanged since 2.0. This version is tested on Python 3.9, 3.10, 3.11, 3.12,
and 2.7.

The next version will drop Python 2 and older Python 3 versions. No new
helpers or API changes are expected. It will focus on updating the packaging
and documentation. It may delete some helpers that now have equivalents in
recent Python versions.

Documentation is in the docs/ directory or read the `online documentation`_.

``constants``
    Country codes, states and provinces.

``containers``
    High-level container objects and dict/list helpers.

``date``
    Date/time helpers.  These currently format strings based on dates.

``html``
    A package of HTML-related helpers.

    ``builder``
        A library for generating HTML tags with smart escaping.  All
        public symbols are imported into ``webhelpers.html``.

    ``tags``
        High-level HTML tags, including form tags, hyperlinks, and 
        Javascript/CSS links.  The ``ModelTags`` class builds input
        tags from database records (for any kind of database).

    ``tools``
        Helpers producing chunks of HTML. Also test-to-HTML and HTML-to-text
        converters.

``misc``
    Miscellaneous helpers that are neither text, numeric, container, or date.

``number``
    Numeric helpers and number formatters.

``text``
    Helpers producing string output, suitable for both HTML and non-HTML
    applications.

For support/question/patches, please use the `Pylons mailing list
<http://groups.google.com/group/pylons-discuss>`_.

Requirements
------------

WebHelpers2 depends on MarkupSafe_ and six_, and it can also use unidecode_ if
you have it installed.


.. _online documentation: http://webhelpers2.readthedocs.org/en/latest/
.. _MarkupSafe: http://pypi.python.org/pypi/MarkupSafe
.. _six: http://pypi.python.org/pypi/six
.. _unidecode:  http://python.org/pypi/Unidecode/
