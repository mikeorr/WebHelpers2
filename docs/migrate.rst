.. _migrate:

Migrating from WebHelpers
%%%%%%%%%%%%%%%%%%%%%%%%%

This chapter explains how to migrate an application from WebHelpers to
WebHelpers2.

WebHelpers2 has a narrower scope than WebHelpers. It deletes some subsystems
that were the hardest to support or had dependencies on the obsolete Pylons
framework, so that the most popular and smallest parts of WebHelpers could be
ported to Python 3. The parts that remain focus on HTML generation, text
processing, value formatting, container objects, and statistics. All helpers
were reviewed, and several were renamed and a few changed their argument
signatures. Several were deleted because they were little used, no longer
needed in Python 2.6+, or depended on deleted modules.

Global changes
==============

The top-level package was renamed to ``webhelpers2``, so you'll have to change
your imports. (The reason it was renamed was to avoid breaking older
applications that are still using the WebHelpers API but were not pinned to a
specific version of it.)

The test suite is PyTest rather than Nose. All doctests have been converted to
unit tests. The remaining code examples in the documentation are meant solely
for documentation. (The doctests in the HTML subpackage have not been
converted yet because a larger rewrite of that subpackage is pending.)

Deleted modules
===============

Deleted the **feedgenerator** module. PyPI has a feedgenerator_ distribution
that is a more basic port of the Django original, and a feedgen_ distro that's
more modular. Neither of them support GeoRSS as the WebHelpers module did.
(This module was dropped because it was significant work to periodically merge
updates from the Django original, and the WebHelpers developers are not
newsfeed experts and couldn't really evaluate the patches.) You can also
generate newsfeeds with a simple template; XXX TODO here are Mako functions for
that generate Atom and RSS with GeoRSS.

Deleted the **html.converters**, **markdown**, and **textile** modules.
For Markdown, see the markdown_ and markdown2_ distros on PyPI. For Textile,
see the textile_ distro. The remaining helpers in the 'converters' module were
moved to 'webhelpers.html.tools'. Renamed:

    * format_paragraphs() -> ``text_to_html()`` (in 'webhelpers.html.tools')
    * render() -> ``html_to_text()`` (in 'webhelpers.html.tools')

Deleted the **html.grid** and **html.grid_demo** modules. These were other
third-party modules that were ill-advisedly included in WebHelpers.  The author
Marcin Lulek (Ergo^) has stated his intention to release it on PyPI; it does
not appear to be there yet.

Deleted the **media**.  The ``choose_height()`` helper was moved to
'webhelpers.misc'. The 'get_dimensions()' helper has equivalents on PyPI; see
the dimensions_ and imagefacts_ distros, and the Pillow_ imaging library.

Deleted the **mimehelper** module. It had undeclared Pylons dependencies
and didn't really do much useful.

Deleted the **paginate** module. Its author Christoph Haas has released a
newer and more modular version as the 'paginate' distro on PyPI. It refactors
Deleted the URL generation API and SQLAlchemy support, so you will have to make those
changes in your appliation.

Deleted the **pylonslib** subpackage. Pylons is obsolete and will not be
ported to Python 3. For Pyramid applications, equivalents to 'flash' and
'secure_form' are in the Pyramid session support. For CSS/Javascript
minification, see the several third-party implementations. 'grid' has been
deprecated since WebHelpers 1.0b1.

Deleted the **util** module. Most of it was support functions for other
helpers, and most of that was either obsolete or superceded by the Python
standard library, MarkupSafe, or newer versions of WebOb. (This leaves
*update_params()* without a home; it’s currently in the 'unfinished' directory in
Deleted the source distribution until a location is determined.)


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


webhelpers.html
===============

A rewrite of the HTML subpackage is pending. It's still unclear whether it will be
compatible, or require changing imports, or require changing helper names and
arguments. The MarkupSafe dependency will probably be retained, although there
may be a callback to provide your own implementation. MarkupSafe 0.16
dropped compatibility with Python 3.0 - 3.2 (it's still compatible with 2.6,
2.7, or 3.3), so if you're running under an early version of Python 3 you'll
have to use MarkupSafe 0.15. (But WebHelpers2 is not yet compatible with Python
3 anyway.)

All tag-generating helpers now convert underscores to hyphens in attribute
names. This is to support HTML5 "data-" attributes as keyword args. Trailing
underscores are still removed ("class\_" -> "class"). This was implemented at
the lowest level, so all the low-level helpers in the 'builder' module and the
high-level helpers in the 'tags' module have this feature.


webhelpers.html.tags
--------------------

The ``image()`` helper no longer accepts args 'path' or 'use_pil', and raises
TypeError if they are specified. These depended on the 'media' module which was
deleted. To perform the equivalent, write a wrapper function that uses one of
the 'media' alternatives discussed above to parse the dimensions from an image
file. A future version of WebHelpers2 may reintroduce an API for this, but you
would have to supply your own callback function to do the parsing.

Deleted 'required_legend()'. Put equivalent HTML in your template manually.

Deleted the 'Doctype' class. Use simply "<!DOCTYPE html>" for HTML 5.

Deleted the sample CSS stylesheet.


webhelpers.html.tools
---------------------

Deleted the 'highlighter' arg in ``highlight()``. It has been deprecated since
WebHelpers 1.0b2.


webhelpers.misc
===============

Renamed helpers:

    * convert_or_none() -> ``convert()``
    * subclasses_only() -> ``subclasses_of()``

Deleted 'all()', 'any()', and 'no()'. For the first two without a predicate,
use the Python builtins ``all()`` or ``any()`` (added in Python 2.5). For 'no'
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


webhelpers.text
===============

Changed the argument signature of ``series()``. The items are now positional
args instead of an iterable, and the keyword args are renamed to ``conj`` and
``strict``.



.. _dimensions: http://pypi.python.org/pypi/dimensions
.. _feedgenerator: http://pypi.python.org/pypi/feedgenerator
.. _feedgen: http://pypi.python.org/pypi/feedgen
.. _imagefacts: http://pypi.python.org/pypi/imagefacts
.. _markdown: http://pypi.python.org/pypi/markdown
.. _markdown2: http://pypi.python.org/pypi/markdown2
.. _Pillow: http://pypi.python.org/pypi/Pillow
.. _paginate: http://pypi.python.org/pypi/paginate
.. _textile: http://pypi.python.org/pypi/textile
