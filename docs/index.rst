WebHelpers2
%%%%%%%%%%%
:Version: |release|, released 2012-01-29
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

**WebHelpers2** narrows the focus to a core set of utilities that are most widely
used, relevant to the new Pyramid framework, and easiest to maintain and port
to Python 3. In particular it keeps the HTML builder and HTML tag functions,
and most of the text-processing, number formatting, statistics, and date
functions. It removes the large third-party subpackages and some obsolete or
little-used helpers. See :ref:`changes-in-webhelpers2` for a list of new
features, deletions and incompatible changes. See the :ref:`todo` for the 
goals for 2.0 and a list of helpers are still being considered for deletion.

WebHelpers2 depends on MarkupSafe_, and it can use Unidecode_ if it's installed.
An extensive test suite for doctest and Nose is included.
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
