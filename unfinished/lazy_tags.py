from __future__ import unicode_literals

from webhelpers2.html import HTML

class Tag(list):
    """Lazily-rendered tag.

    You can set my HTML attributes and content incrementally and pass me to a
    template.  Call ``str`` on me to render the HTML.

    Instance attributes:

    * **attrs**: Dict of HTML attributes.
    * **content**: List of content items.
    * **nl**: If true, render a newline after the opening tag, after each
      content item, and after the closing tag. Default is false.
      can force newlines by setting the class attribute **nl** to true.

    Class attributes:

    * **render_if_empty**: This affects what happens if the tag has no content.
      If true (default), render it as normal. If false, suppress the tag and
      render the empty string instead.
    * **nl**: Default value for ``self.nl``.
    """
    render_if_empty = True
    nl = False

    def __init__(self, name, *content, **attrs):
        """Constructor.

        * **name**: The tag name.
        * **\*content**: Initial content.
        * **\*\*attrs**: Initial HTML attributes.
        """
        super(Tag, self).__init__()
        self.name = name
        self.attrs = attrs
        self.content = list(content)

    def child(self, child):
        """Append an item to the content.
        
        Equivalent to ``self.content.append()``.
        """
        self.content.append(child)

    def __html__(self):
        if not (self.content or self.render_if_empty):
            return HTML.EMPTY
        return HTML.tag(self.name, _nl=self.nl, *self.content, **self.attrs)

    __str__ = __html__


class UL(Tag):
    name = "ul"
    nl = True
    render_if_empty = False

    def __init__(self, **attrs):
        super(UL, self).__init__(self.name, **attrs)

    def item(self, item, **attrs):
        """Add a list item.

        I wrap the item in an <li> tag and append it to the content.
        Keyword args become <li> attributes.
        """
        item = self.__class__("li", item, **attrs)
        self.content.append(item)


class OL(UL):
    name = "OL"


class DL(UL):
    name = "DL"

    def item(self, term, definition):
        """Append a definition item.

        * **term**: The term.
        * **definition**: The definition.

        I wrap the term in a <dt> and the definition in a <dd>, and append them
        to the list content.

        Keyword attributes are not currently allowed because it's unclear
        which tag they should apply to.
        """
        dt = self.__class__("dt", term)
        dd = self.__class__("dd", definition)
        self.content.append(dt)
        self.content.append(dd)


