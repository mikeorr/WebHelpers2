:mod:`webhelpers2.html.builder`
================================================

.. automodule:: webhelpers2.html.builder

.. currentmodule:: webhelpers2.html.builder

HTML Builder provides:

* an ``HTML`` object that creates (X)HTML tags in a Pythonic way.

* a ``literal`` class used to mark strings containing intentional HTML markup.

* a smart escaping mechanism that preserves literals but
  escapes other strings that may accidentally contain markup characters ("<",
  ">", "&", '"', "'") or malicious Javascript tags.  Escaped strings are
  returned as literals to prevent them from being double-escaped later.

The builder uses markupsafe_ and follows Python's unofficial
``.__html__`` protocol, which Mako_, Chameleon_, Pylons, and some other
packages also follow.  These features are explained in the next section.

Literals
--------

.. autoclass:: literal(s, encoding=None, errors=strict')
   :members:  __new__, escape, unescape, striptags


The HTML generator
------------------

The ``HTML`` global is an instance of the ``HTMLBuilder`` class.
Normally you use the global rather than instantiating it yourself.

.. autoclass:: HTMLBuilder

   .. automethod:: __call__
   .. automethod:: __getattr__
   .. automethod:: tag
   .. automethod:: comment
   .. automethod:: cdata
   .. automethod:: render_attrs

   **The following class attributes are literal constants:**

   .. data:: EMPTY

      The empty string as a literal.

   .. data:: SPACE

      A single space as a literal.

   .. data:: TAB2

      A 2-space tab as a literal.

   .. data:: TAB4

      A 4-space tab as a literal.

   .. data:: NL

      A newline ("\\n") as a literal.

   .. data:: NL2

      Two newlines as a literal.

   .. data:: BR

      A literal consisting of one "<br />" tag.

   .. data:: BR2

      A literal consisting of two "<br />" tags.


   **The following class attributes affect the behavior of the ``tag``
   method:**

   .. data:: void_tags

      The set of tags which can never have content. These are rendered
      in self-closing style; e.g., '<br />'. See
      `About XHTML and HTML`_ below.

   .. data:: boolean_attrs

      The set of attributes which are rendered as booleans. E.g.,
      ``disabled=True`` renders as 'disabled="disabled"', while
      ``disabled=False`` is not rendered at all.

      The default set is conservative; it includes only "defer",
      "disabled", "multiple", and "readonly".

   .. data:: compose_attrs

      A dict of attributes whose value may have string-delimited
      components.  The keys are attribute names and the values are
      delimiter literals. The default configuration supports the "class"
      and "style" attributes.

   .. data:: literal

      The ``literal`` class that will be used internally to generate
      literals. Changing this does not automatically affect the constant
      attributes (EMPTY, NL, BR, etc).


About XHTML and HTML
--------------------

This builder always produces tags that are valid as *both* HTML and XHTML.
"Void" tags -- those which can never have content like ``<br>`` and ``<input>``
-- are written like ``<br />``, with a space and a trailing ``/``.

*Only* void tags get this treatment.  The library will never, for
example, produce ``<script src="..." />``, which is invalid HTML and
legacy browsers misinterpret it as still being open.  Instead
the builder will produce ``<script src="..."></script>``.

The `W3C HTML validator <http://validator.w3.org/>`_ validates these
constructs as valid HTML Strict.  It does produce warnings, but those
warnings warn about the ambiguity if this same XML-style self-closing
tags are used for HTML elements that are allowed to take content (``<script>``,
``<textarea>``, etc).  This library never produces markup like that.

Rather than add options to generate different kinds of behavior, we
felt it was better to create markup that could be used in different
contexts without any real problems and without the overhead of passing
options around or maintaining different contexts, where you'd have to
keep track of whether markup is being rendered in an HTML or XHTML
context.

If you _really_ want void tags without training slashes (e.g.,
``<br>``), you can abuse ``_closed=False`` to produce them.

Functions
---------

.. function:: escape(s)

   Same as ``literal.escape(s)``.

.. autofunction:: lit_sub

.. function:: url_escape(s, safe='/')

    Urlencode the path portion of a URL. This is the same function as
    ``urllib.quote`` in the Python standard library. It's exported here
    with a name that's easier to remember.

The ``markupsafe`` package has a function ``soft_unicode`` which converts a
string to Unicode if it's not already. Unlike the Python builtin ``unicode()``,
it will not convert ``Markup`` (``literal``) to plain Unicode, to avoid
overescaping. This is not included in webhelpers2 but you may find it useful.


.. _markupsafe: http://pypi.python.org/pypi/markupsafe
.. _Mako: http://www.makotemplates.org/
.. _Chameleon: http://chameleon.readthedocs.org/
