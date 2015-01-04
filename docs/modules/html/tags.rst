:mod:`webhelpers2.html.tags`
================================================

.. automodule:: webhelpers2.html.tags

.. currentmodule:: webhelpers2.html.tags

Form tags
---------

.. autofunction:: form

.. autofunction:: end_form

.. autofunction:: text

.. autofunction:: textarea

.. autofunction:: hidden

.. autofunction:: file

.. autofunction:: password

.. autofunction:: checkbox

.. autofunction:: radio

.. autofunction:: submit

Select and Options helpers
++++++++++++++++++++++++++

The ``select`` helper creates a dropdown selection box. It's mostly a wrapper
around the ``Options`` class, which in turn is a container of ``Option`` and/or
``OptGroup`` instances.

You can call ``Options.render`` on its own to create a set of options. This can
be useful to manually place options inside an HTML <select> in a template, or
in an HTML 5 <datalist>.

There are four main differences compared to WebHelpers:

1. The availability of ``Options.render``.
2. API overhaul in ``Options``, ``Option``, and ``OptGroup``, including "label
   before value" argument order.
3. If an option has no 'value' argument or it's identical to the label, then the
   ``Option.value`` attribute will be None, the HTML <option> tag will have no
   'value' attribute, and on form submission the parameter will be the same as
   the label. We originally believed the 'value' attribute was required in HTML,
   but it's optional in HTML 5 and 4.0.1. This is distinct from a value of
   ``""`` (the empty string), which renders as is and on form submission the
   parameter will be empty or missing.
4. **[Late change in 2.0rc3]**
   The ``options`` argument to ``select`` no longer accepts lists of lists,
   lists of tuples, or other complex data structures. You can no longer pass
   ``[(myvalue, mylabel)]`` or ``[(optgroup_label, options)]``; these
   now raise ``TypeError``. Instead you should explicitly build up an
   ``Options`` instance and pass it. This restriction was made for simplicity,
   reliability, and maintainability.

.. autofunction:: select

.. autoclass:: Options
   :members: __init__, add_option, add_optgroup, render

.. autoclass:: Option
   :members: __init__

.. autoclass:: OptGroup
   :members: __init__, add_option


:class:`ModelTags` class
++++++++++++++++++++++++

.. autoclass:: ModelTags
   :members:
   :special-members: __init__


Hyperlinks
----------

.. autofunction:: link_to

.. autofunction:: link_to_if

.. autofunction:: link_to_unless

:class:`Link` class
+++++++++++++++++++

.. autoclass:: Link

   .. automethod:: __init__



Table tags
----------

.. autofunction:: th_sortable


Other non-form tags
-------------------

.. autofunction:: ol

.. autofunction:: ul

.. autofunction:: image

.. attribute:: BR

    Same as ``HTML.BR``. 
    A break tag ("<br />") followed by a newline. This is a literal 
    constant, not a function.


Head tags and document type
---------------------------

.. autofunction:: stylesheet_link

.. autofunction:: javascript_link

.. autofunction:: auto_discovery_link


Utilities
---------

.. autofunction:: _make_safe_id_component
