"""Helpers that are neither text, numeric, container, or date.
"""

import itertools
import traceback
import types
import warnings

def choose_height(new_width, width, height):
    """Calculate a proportional height for scaling an image. Given the image's
    existing width and height and proposed new width, return the height that
    preserves the width:height ratio of the original.
    """
    proportion = float(height) / float(width)
    return int(new_width * proportion)

def count_true(seq, pred=lambda x: x):
    """How many elements is ``pred(elm)`` true for?

    With the default predicate, this counts the number of true elements.

    This is equivalent to the ``itertools.quantify`` recipe, which I couldn't
    get to work.
    """
    ret = 0
    for x in seq:
        if pred(x):
            ret += 1
    return ret

def convert(value, type_):
    """Return the value converted to the type, or None if error.

    ``type_`` may be a Python type or any function taking one argument.
    """
    try:
        return type_(value)
    except Exception:
        return None

def flatten(iterable):
    """Recursively iterate lists and tuples.

    Examples:

    >>> list(flatten([1, [2, 3], 4]))
    [1, 2, 3, 4]
    >>> list(flatten([1, (2, 3, [4]), 5]))
    [1, 2, 3, 4, 5]
    """
    for elm in iterable:
        if isinstance(elm, (list, tuple)):
            for relm in flatten(elm):
                yield relm
        else:
            yield elm



def subclasses_of(class_, it, exclude=None):
    """Extract the subclasses of a class from a module, dict, or iterable.

    Return a list of subclasses found. The class itself will not be included.
    This is useful to collect the concrete subclasses of an abstract base
    class.

    ``class_`` is a class.

    ``it`` is a dict or iterable. If a dict is passed, examine its values,
    not its keys. To introspect the current module, pass ``globals()``. To
    introspect another module or namespace, pass
    ``vars(the_module_or_namespace)``.

    ``exclude`` is an optional list of additional classes to ignore. 
    This is mainly used to exclude abstract subclasses.
    """
    if isinstance(it, dict):
        it = it.itervalues()
    class_types = (type, types.ClassType)
    ignore = [class_]
    if exclude:
        ignore.extend(exclude)
    return [x for x in it if isinstance(x, class_types) and 
        issubclass(x, class_) and x not in ignore]


class NotGiven(object):
    """A default value for function args.

    Use this when you need to distinguish between ``None`` and no value.
    
    Example::
    
        >>> def foo(arg=NotGiven):
        ...     print arg is NotGiven
        ...
        >>> foo()
        True
        >>> foo(None)
        False

    """
    pass


def format_exception(exc=None):
    """Format the exception type and value for display, without the traceback.

    This is the function you always wished were in the ``traceback`` module but
    isn't. It's *different* from ``traceback.format_exception``, which includes
    the traceback, returns a list of lines, and has a trailing newline.

    If you don't provide an exception object as an argument, it will call
    ``sys.exc_info()`` to get the current exception.
    """
    if exc:
        exc_type = type(exc)
    else:
        exc_type, exc = sys.exc_info()[:2]
    lines = traceback.format_exception_only(exc_type, exc)
    return "".join(lines).rstrip()

def deprecate(message, pending=False, stacklevel=2):
    """Issue a deprecation warning.

    ``message``: the deprecation message.

    ``pending``: if true, use ``PendingDeprecationWarning``. If false (default), 
    use ``DeprecationWarning``. Python displays deprecations and ignores
    pending deprecations by default.

    ``stacklevel``: passed to ``warnings.warn``. The default level 2 makes the
    traceback end at the caller's level. Higher numbers make it end at higher
    levels.
    """
    category = pending and PendingDeprecationWarning or DeprecationWarning
    warnings.warn(message, category, stacklevel)
