.. _migrate:

Migrating from WebHelpers
%%%%%%%%%%%%%%%%%%%%%%%%%

This chapter explains how to migrate an application from WebHelpers to
WebHelpers2.

All helpers were reviewed and several were renamed or moved to organize
them better, or changed their arguments to be more useful long term.
WebHelpers2 focuses on the HTML generator and tag library, text
processing, value formatting, container objects, and statistics. Other
large subsystems were deleted if they're available separately on PyPI or
were difficult to maintain. Also deleted were helpers that were
little-used or no longer needed in Python 2.6+, or depended on the
obsolete Pylons framework.

New features are not mentioned here. Please read the rest of the
documentation for them.

Global changes
==============

The top-level package was renamed to ``webhelpers2``, so you'll have to change
your imports. (The reason it was renamed was to avoid breaking older
applications that are still using the WebHelpers API but were not pinned to a
specific version of it.)

The test suite has been changed to PyTest. All doctests have been converted to
unit tests. The remaining code examples in the documentation are solely
for documentation.

webhelpers.constants
====================

No changes.


webhelpers.containers
=====================

Renamed helpers:

    * del_quiet() -> ``del_keys()``
    * except_keys() -> ``copy_keys_except()``
    * extract_keys() -> ``split_dict()``
    * only_some_keys() -> ``copy_keys()``

In all these helpers the ``keys`` argument changed to ``\*keys``, so pass the
keys as positional arguments rather than in an iterable.

Deleted 'get_many()'. It was little used.

Deleted 'Accumulator'. Use ``collections.defaultdict(list)`` in the standard
library or WebOb's 'MultiDict'.

Deleted 'UniqueAccumulator'. Use ``collections.defaultdict(set)`` in the
standard library.

webhelpers.date
===============

No changes.


webhelpers.feedgenerator
========================

Deleted. PyPI has a feedgenerator_ distribution
that is a more basic port of the Django original, and a feedgen_
distribution that's more modular. Neither of them support GeoRSS as the
WebHelpers module did.  (This module was dropped because it was
significant work to periodically merge updates from the Django original,
and the WebHelpers maintainers were not newsfeed experts and couldn't
really evaluate the patches.) You can also generate newsfeeds with a
simple template; XXX TODO here are Mako functions for that generate Atom
and RSS with GeoRSS.


webhelpers.html
===============

No changes at the package level, except for imports from the ``builder``
module that have changed.


builder
-------

``HTML.literal`` is now the ``literal`` class rather than a wrapper
method. As a consequence it no longer accepts multiple positional args.
Use ``HTML(..., lit=True)`` instead.

The 'make_tag()' function was merged into ``HTML.tag()``. 'format_attrs'
was split into ``HTML.optimize_attrs()`` and ``HTML.render_attrs()``.
The 'empty_attrs' global was replaced by ``HTML.void_attrs``.

All tag-generating helpers now convert underscores to hyphens in attribute
names. This is to support HTML5 "data-" attributes as keyword args. Trailing
underscores are still removed ("class\_" -> "class"). This was implemented at
the lowest level, so both ``HTML.tag()`` and all the high-level helpers in
the 'tags' module have this feature.

The code for boolean HTML attributes was rewritten and new boolean
attributes defined; see the :doc:`builder <modules/html/builder>` page
for details.


converters
----------

Deleted. Moved and renamed the following helpers:

* format_paragraphs() -> ``webhelpers2.html.tools.text_to_html()``
* render() -> ``webhelpers2.html.tools.html_to_text()``


grid
----

Deleted the **html.grid** and **html.grid_demo** modules. These were
third-party modules that were ill-advisedly included in WebHelpers.  The
author Marcin Lulek (Ergo^) has released then on PyPI as
webhelpers2_grid_.

Deleted the sample CSS stylesheet.


tags
----

The ``image()`` helper no longer accepts args 'path' or 'use_pil', and raises
TypeError if they are specified. These depended on the 'media' module which was
deleted. To perform the equivalent, write a wrapper function that uses one of
the 'media' alternatives discussed below to parse the dimensions from an image
file. A future version of WebHelpers2 may reintroduce an API for this, but you
would have to supply your own callback function to do the parsing.

Deleted 'required_legend()', 'title()', and 'xml_declaration()'. Use
manual HTML.

Deleted the 'Doctype' class. Use simply "<!DOCTYPE html>" for HTML 5.

Deleted 'convert_boolean_attrs()' and 'css_classes()'. The HTML builder
now does these itself.


tools
-----

Deleted the 'highlighter' arg in ``highlight()``. It has been deprecated since
WebHelpers 1.0b2.



webhelpers.markdown
===================

Deleted. Use the markdown_ or markdown2_ distributions on PyPI.


webhelpers.media
================

Deleted.

The ``choose_height()`` helper was moved to 'webhelpers.misc'.

The 'get_dimensions()' helper has equivalents on PyPI; see the
dimensions_ and imagefacts_ distributions, and the Pillow_ imaging library.


webhelpers.mimehelper
=====================

Deleted. It had undeclared Pylons dependencies and didn't really do much
useful.


webhelpers.misc
===============

Renamed helpers:

* convert_or_none() -> ``convert()``
* subclasses_only() -> ``subclasses_of()``

Deleted 'all()', 'any()', and 'no()'. For the first two without a predicate,
use the Python builtins ``all()`` or ``any()``. For 'no()'
or to use a predicate, copy the WebHelpers implementations (which were borrowed
from Python's ``itertools`` documentation).

Deleted 'format_number()'. To display a number with thousands separators, use
``"{:,}".format(12346)`` (which always uses commas) or ``"{:n}".format(12345)``
(which uses the locale-specific separator). The former was added in Python 2.7.

Deleted 'DeclarativeException'. It was too specialized for general use.

Deleted 'OverwriteError'. Python 3 may add an exception for this; otherwise you
can use one of the stdlib exceptions or make your own.


webhelpers.number
=================

Deleted the 'Stats' and 'SimpleStats' classes. The underlying function-based
helpers remain.


webhelpers.paginate
===================

Deleted. Its author Christoph Haas has released a newer and more modular
version as the paginate_ and paginate_sqlalchemy_ distributions on PyPI.

webhelpers.pylonslib
====================

Deleted the subpackage. Pylons is obsolete and will not be
ported to Python 3. For Pyramid applications, equivalents to 'flash' and
'secure_form' are in the Pyramid session support. For CSS/Javascript
minification, see the several third-party implementations. 'grid' has
been deprecated since WebHelpers 1.0b1.


webhelpers.text
===============

Changed the argument signature of ``series()``. The items are now positional
args instead of an iterable, and the keyword args are renamed to ``conj`` and
``strict``.


webhelpers.textile
==================

Deleted. Use the textile_ distribution on PyPI.


webhelpers.util
===============

Deleted. Most of it was support functions for other helpers, and most of
that was either obsolete or superceded by the Python standard library,
MarkupSafe, or newer versions of WebOb. 

This leaves *update_params()* without a home; it’s currently in the
'unfinished' directory in the source distribution until a location is
determined.

.. include:: include.rst
