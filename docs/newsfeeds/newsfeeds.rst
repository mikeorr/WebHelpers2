.. _newsfeed:

Newsfeed templates
==================

WebHelpers2 doesn't include WebHelpers' feedgenerator module, so here's
a simple alternative using Mako templates. It's based on the output of
feedgenerator converted to Mako templates. This example uses GeoRSS so
each item has a latitude/longitude.  The templates may not support all of
feedgenerator's features but it's sufficient for basic sites.

To run the example:

1. Create a directory and chdir to it.
2. Download "atom.mako", "rss.mako", and "newsfeeds.py" below. The
   templates must be in the current directory.
3. Install Mako_.
4. Run "python newsfeeds.py".

It will put the output files in the current directory: "news.atom" and
"news.mako".

If you use the "--debug" option it will also write the compiled
templates to files: "news.atom.py" and "news.rss.py".


Atom template
-------------

Download: :download:`atom.mako`

.. literalinclude:: atom.mako
   :language: html+mako

RSS template
------------

Download: :download:`rss.mako`

.. literalinclude:: rss.mako
   :language: html+mako

The script
----------

Download :download:`newsfeeds.py`

.. literalinclude:: newsfeeds.py


.. include:: ../include.rst
