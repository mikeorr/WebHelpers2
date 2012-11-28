"""Functions that convert from text markup languages to HTML and back.

"""
import re

from webhelpers.html import HTML, escape, literal, lit_sub

# render() and sanitize() are imported from the private module 'render'.
from webhelpers.html.render import render, sanitize

__all__ = [
    "format_paragraphs",
    "nl2br",
    "render",
    "sanitize",
    ]

_universal_newline_rx = re.compile(R"\r\n|\n|\r")  # All types of newline.
_paragraph_rx = re.compile(R"\n{2,}")  # Paragraph break: 2 or more newlines.
br = HTML.br() + "\n"

def nl2br(text):
    """Insert a <br /> before each newline.
    """
    if text is None:
        return literal("")
    text = lit_sub(_universal_newline_rx, "\n", text)
    text = HTML(text).replace("\n", br)
    return text

def format_paragraphs(text, preserve_lines=False):
    """Convert text to HTML paragraphs.

    ``text``:
        the text to convert.  Split into paragraphs at blank lines (i.e.,
        wherever two or more consecutive newlines appear), and wrap each
        paragraph in a <p>.

    ``preserve_lines``:
        If true, add <br />  before each single line break
    """
    if text is None:
        return literal("")
    text = lit_sub(_universal_newline_rx, "\n", text)
    paragraphs = _paragraph_rx.split(text)
    for i, para in enumerate(paragraphs):
        if preserve_lines:
            para = HTML(para)
            para = para.replace("\n", br)
        paragraphs[i] = HTML.p(para)
    return "\n\n".join(paragraphs)

