WebHelpers2
%%%%%%%%%%%
:Version: |release|, released XXXX-XX-XX
:PyPI: http://pypi.python.org/pypi/WebHelpers2
:Docs: https://webhelpers2.readthedocs.org/en/latest/
:Source: https://github.com/mikeorr/WebHelpers2 (Git)

.. image:: _static/webhelpers-logo.png
   :width: 100px
   :height: 100px
   :alt: WebHelpers Logo
   :align: right

**WebHelpers2** is the successor to the widely-used WebHelpers_ utility functions.
The name was changed to avoid breaking applications that depend on
the 1.x API but are not formally pinned to it.

*This documentation is in flux. It may not fully reflect changes since 1.3, and
it may have internal inconsistencies.*

**WebHelpers2** narrows the focus to a core set of utilities that are most widely
used, relevant to the new Pyramid framework, and easiest to maintain and port
to Python 3. In particular it keeps the HTML builder and HTML tag functions,
and most of the text-processing, number formatting, statistics, and date
functions. It removes the large third-party subpackages: feedgenerator, grid, 
paginage, markdown, and textile. These are or will be available as separate
PyPI distributions maintained by their own authors. Some other helpers were
deleted because they depended on Pylons, were superceded by standard library
functions (as of Python 2.6), were little-used, or seemed like good ideas at the
time.

**Version 2.0a1** works on Python 2.6 and 2.7. The final will support Python 3.
For a roadmap, things being considered for deletion, and ways you can help, see
the `TODO <todo.html>`. WebHelpers2 depends on MarkupSafe_, and can use
Unidecode_ if it's installed.  An extensive test suite for doctest and Nose is
included.

For support/questions/patches, please use the pylons-discuss_ mailing list.

.. toctree::
   :maxdepth: 2

   contents

.. toctree::
   :maxdepth: 1

   whats_new
   changelog
   third_party
   todo
   development
   todo

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _What's New: whats_new.html
.. _MarkupSafe: http://pypi.python.org/pypi/MarkupSafe
.. _Routes: http://routes.groovie.org/
.. _Unidecode: http://pypi.python.org/pypi/Unidecode/
.. _WebOb: http://pythonpaste.org/webob/
.. _Pylons: http://pylonshq.com/
.. _pylons-discuss: http://groups.google.com/group/pylons-discuss
.. _WebHelpers: http://pypi.python.org/pypi/WebHelpers
