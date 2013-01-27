"""HTML generation helpers.

All public objects in the ``webhelpers2.html.builder`` subpackage are also
available in the ``webhelpers2.html`` namespace.  Most programs will want
to put this line in their code::

    from webhelpers2.html import *

Or you can import the most frequently-used objects explicitly::

    from webhelpers2.html import HTML, escape, literal
"""

from webhelpers2.html.builder import *
