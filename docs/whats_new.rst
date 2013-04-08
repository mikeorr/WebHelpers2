.. _changes-in-webhelpers2:

Changes in WebHelpers2
%%%%%%%%%%%%%%%%%%%%%%%%%

Changes since beta 1
--------------------

Beta 3:
Merge 'html.converters' submodule into 'html.tools'. Rename 'format_paragraphs'
to 'text_to_html' and fix bug so it returns a literal. Rename 'render' to
'html_to_text'. Document 'html_to_text' and 'sanitize'.

Beta 3:
Rename 'del_quiet' to 'del_keys' and change to take keys as positional args.
Rename 'extract_keys' to 'split_dict'.

Beta 3:
Delete several helpers from various modules: 'get_many', 'format_number',
'required_legend', 'all', 'any', 'no'.
Delete the 'Stats' and 'SimpleStats' container classes (the underlying
function-based helpers remain).
Delete the sample CSS stylesheet.

Beta 2: 
All HTML tag helpers now convert underscores to hyphens in attribute
names. This is to support HTML5 "data-" attributes as keyword args. Trailing
underscores are still removed ("class\_" -> "class").

Beta 2:
Delete 'highlighter' arg in 'webhelpers2.html.tools.highlight()'. It has been
deprecated since WebHelpers 1.0b2.

Deleted modules
---------------

Most of the large third-party modules are deleted because they were the hardest
parts of WebHelpers to support since the WebHelpers maintainer was not expert
in those areas, and every upstream release had to be patched to fit into
WebHelpers. Some of the deleted modules are available as standalone
distributions in PyPI.

Deleted **webhelpers.feedgenerator**. Alex Metaireau has released feedgenerator_, an
independent port of the same Django original. We're in discussion with the 
author about merging the WebHelpers feedgenerator enhancements into his
distribution. Note that this version may follow Django's convention of
putting longitude first in latitude-longitude tuples. WebHelpers
feedgenerator was switchable but defaulted to latitude first, as is more common. 

Deleted **webhelpers.html.grid** and its derivatives (webhelpers.html.grid_demo,
webhelpers.pylonslib.grid). Its author Ergo^ has said he will release a
standalone distribution.

Deleted **webhelpers.markdown** and **webhelpers.textile** and their wrappers
``markdown()`` and ``textilize()`` in webhelpers.html.converters.
These had stagnated behind their upstream versions, and their wrappers hardly
did anything.

Deleted **webhelpers.mimehelper**. It had undeclared Pylons dependencies and
didn't really do much useful.

Deleted **webhelpers.paginate**. Its author Christoph Haas has updated the
standalone paginate_ distribution.

Deleted **webhelpers.pylonslib** and all its submodules (flash, grid, minify,
secure_form). These were all designed for Pylons 1, which has been superceded
by Pyramid.

Deleted **webhelpers.util**. Most of it was support functions for other helpers,
and most of that was either obsolete or superceded by the Python standard
library, MarkupSafe, or newer versions of WebOb. (This leaves *update_params()*
without a home; it's currently in the unfinished directory until a location is
determined.)

Changes in webhelpers.containers
--------------------------------

Deleted 'Accumulator'.  Use ``collections.defaultdict(list)`` in stdlib or
WebOb's MultiDict.  

Deleted 'UniqueAccumulator'.  Use ``collections.defaultdict(set)`` in stdlib.

Changes in webhelpers.html.tags
-------------------------------

Deleted 'Doctype'. Use simply "<!DOCTYPE html>" for HTML 5.

Changes in webhelpers.html.misc
-------------------------------

Renamed 'subclasses_only()' to ``subclasses_of()``.

Deleted 'DeclarativeException'. It was too specialized for general use.

Deleted 'OverwriteError'. Python 3 may add an exception for this; otherwise you
can use one of the stdlib exceptions or make your own.


.. _feedgenerator: http://pypi.python.org/pypi/feedgenerator/1.2.1
.. _paginate: http://pypi.python.org/pypi/paginate/0.4.0
