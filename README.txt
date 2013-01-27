WebHelpers2
++++++++++++

WebHelpers2 provides functions useful in web applications: generating HTML tags,
showing results a pageful at a time, etc.  It may be used with any web
framework or template engine.  A brief outline is below, but see the
documentation and module docstrings for a more complete list.

``constants``
    Country codes, states and provinces.

``containers``
    High-level container objects and dict/list helpers.

``date``
    Date/time helpers.  These currently format strings based on dates.

``html``
    A package of HTML-related helpers.

    ``html.builder``
        A library for generating HTML tags with smart escaping.  All
        public symbols are imported into ``webhelpers.html``.

    ``converters``
        Text-to-HTML converters.

    ``tags``
        High-level HTML tags, including form tags, hyperlinks, and 
        Javascript/CSS links.  The ``ModelTags`` class builds input
        tags from database records (for any kind of database).

    ``tools``
        Helpers producing chunks of HTML.

``media``
    Helpers for images, PDFs, etc.

``misc``
    Miscellaneous helpers that are neither text, numeric, container, or date.

``number``
    Numeric helpers and number formatters.

``text``
    Helpers producing string output, suitable for both HTML and non-HTML
    applications.

WebHelpers is package aimed at providing helper functions for use within web
applications.

These functions are intended to ease web development with template languages by
removing common view logic and encapsulating it in re-usable modules as well as
occasionally providing objects for use within controllers to assist with common
web development paradigms.

For support/question/patches, please use the `Pylons mailing list
<http://groups.google.com/group/pylons-discuss>`_.

Requirements
------------

WebHelpers2 depends on MarkupSafe_, and it can also use unidecode_ if you have
it installed.


.. _MarkupSafe: http://pypi.python.org/pypi/MarkupSafe
.. _unidecode:  http://python.org/pypi/Unidecode/
