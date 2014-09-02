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

.. autofunction:: select

.. autoclass:: Options
   :members:

.. autoclass:: Option
   :members:

.. autoclass:: OptGroup
   :members:


:class:`ModelTags` class
--------------------------

.. autoclass:: ModelTags
   :members:


Hyperlinks
----------

.. autofunction:: link_to

.. autofunction:: link_to_if

.. autofunction:: link_to_unless


Table tags
----------

.. autofunction:: th_sortable


Other non-form tags
-------------------

.. autofunction:: ol

.. autofunction:: ul

.. autofunction:: image

.. attribute:: BR

    A break tag ("<br />") followed by a newline. This is a literal 
    constant, not a function.


Head tags and document type
---------------------------

.. autofunction:: stylesheet_link

.. autofunction:: javascript_link

.. autofunction:: auto_discovery_link


Lazy-rendering tags
-------------------

.. autoclass:: Link

   .. automethod:: __init__


Utilities
---------

.. autofunction:: _make_safe_id_component
