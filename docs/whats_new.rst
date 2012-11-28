What's New in WebHelpers2
%%%%%%%%%%%%%%%%%%%%%%%%%

This is a high-level overview of recent changes. **Incompatible changes are
in boldface;** these may require modifying your application.  See `Changelog
<changelog.html>`_ for the full changelog.

Version 2.0a1
=============

Incompatible changes from WebHelpers 1.3
----------------------------------------

**Delete ``webhelpers.feedgenerator``.**  A standalone feedgenerator_ package
is on PyPI. The reason for removing it is that it's a lot of work to port changes
from the upstream Django version and reconcile them with the WebHelpers
patches. The current WebHelpers maintainers aren't GIS or RSS experts so we
can't effectively evaluate the upstream changes and user pull requests.
Alexis Metaireau has released a standalone feedgenerator_ package on PyPI,
which is an independent port of Django's feed generator. We are still
evaluating it but hope to recommend it or another package soon. It does not
have the WebHelpers enhancements, however. We're in discussion with the author
about getting these enhancements merged in in a way satisfactory to both
WebHelpers users and the package's other users. The biggest issue is that 
``feedgenerator`` probably expects latitude-longitude pairs per Django's
convention, while ``webhelpers.feedgenerator`` defaults to the more common (and
RSS required) longitude-latitude format and can switch to either style.

**Delete ``webhelpers.html.grid`` and derivatives
(``webhelpers.html.grid_demo``, ``webhelpers.pylonslib.grid``).**

**Delete ``webhelpers.markdown`` and ``webhelpers.textile`` and their front-end
helpers ``markdown()`` and ``textilize()`` in ``webhelpers.html.converters``.**

**Delete ``webhelpers.pylonslib`` and all its submodules (flash, grid, minify,
secure_form).**

.. _feedgenerator: http://pypi.python.org/pypi/feedgenerator/1.2.1
