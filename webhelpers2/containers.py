"""Container objects, and helpers for lists and dicts.

This would have been called this "collections" except that Python 2 can't
import a top-level module that's the same name as a module in the current
package.
"""

import collections
import sys

from webhelpers2.misc import NotGiven

class DumbObject(object):
    """A container for arbitrary attributes.

    Usage::
    
        >>> do = DumbObject(a=1, b=2)
        >>> do.b
        2
    
    Alternatives to this class include ``collections.namedtuple`` in Python
    2.6, and ``formencode.declarative.Declarative`` in Ian Bicking's FormEncode
    package.  Both alternatives offer more features, but ``DumbObject``
    shines in its simplicity and lack of dependencies.

    """
    def __init__(self, **kw):
        self.__dict__.update(kw)


class Counter(object):
    """I count the number of occurrences of each value registered with me.
    
    Call the instance to register a value. The result is available as the
    ``.result`` attribute.  Example::

        >>> counter = Counter()
        >>> counter("foo")
        >>> counter("bar")
        >>> counter("foo")
        >>> sorted(counter.result.items())
        [('bar', 1), ('foo', 2)]

        >> counter.result
        {'foo': 2, 'bar': 1}

    To see the most frequently-occurring items in order::

        >>> counter.get_popular(1)
        [(2, 'foo')]
        >>> counter.get_popular()
        [(2, 'foo'), (1, 'bar')]

    Or if you prefer the list in item order::

        >>> counter.get_sorted_items()
        [('bar', 1), ('foo', 2)]
    """

    def __init__(self):
        self.result = collections.defaultdict(int)
        self.total = 0  # Number of times instance has been called.

    def __call__(self, item):
        """Register an item with the counter."""
        self.result[item] += 1
        self.total += 1

    def get_popular(self, max_items=None):
        """Return the results as as a list of ``(count, item)`` pairs, with the
        most frequently occurring items first.

        If ``max_items`` is provided, return no more than that many items.
        """
        data = [(x[1], x[0]) for x in self.result.iteritems()]
        data.sort(key=lambda x: (sys.maxint - x[0], x[1]))
        if max_items:
            return data[:max_items]
        else:
            return data

    def get_sorted_items(self):
        """Return the result as a list of ``(item, count)`` pairs sorted by item.
        """
        data = self.result.items()
        data.sort()
        return data

    def correlate(class_, iterable):
        """Build a Counter from an iterable in one step.

        This is the same as adding each item individually.
        """
        counter = class_()
        for elm in iterable:
            counter(elm)
        return counter
    correlate = classmethod(correlate)


def unique(it):
    """Return a list of unique elements in the iterable, preserving the order.

    Usage::

        >>> unique([None, "spam", 2, "spam", "A", "spam", "spam", "eggs", "spam"])
        [None, 'spam', 2, 'A', 'eggs']
    """
    seen = set()
    ret = []
    for elm in it:
        if elm not in seen:
            ret.append(elm)
            seen.add(elm)
    return ret

def copy_keys(dic, *keys):
    """Return a copy of the dict with only the specified items present.  
    
    ``dic`` may be any mapping. The return value is always a Python dict.
    """
    ret = {}
    for key in keys:
        ret[key] = dic[key]   # Raises KeyError.
    return ret

def copy_keys_except(dic, *keys):
    """Return a copy of the dict without the specified items.
    """
    ret = dic.copy()
    for key in keys:
        try:
            del ret[key]
        except KeyError:
            pass
    return ret

def split_dict(dic, *keys):
    """Return two copies of the dict.  The first will contain only the
    specified items.  The second will contain all the *other* items from the
    original dict.

    Example::

        >>> split_dict({"From": "F", "To": "T", "Received", R"}, "To", "From") 
        ({"From": "F", "To": "T"}, {"Received": "R"})
    """
    for k in keys:
        if k not in dic:
            raise KeyError("key {!r} is not in original mapping".format(k))
    r1 = {}
    r2 = {}
    for k, v in dic.items():
        if k in keys:
            r1[k] = v
        else:
            r2[k] = v
    return r1, r2

def ordered_items(dic, key_order, other_keys=True, default=NotGiven):
    """Like ``dict.iteritems()`` but with a specified key order.

    Arguments:

    * ``dic`` is any mapping.
    * ``key_order`` is a list of keys.  Items will be yielded in this order.
    * ``other_keys`` is a boolean.
    * ``default`` is a value returned if the key is not in the dict.

    This yields the items listed in ``key_order``.  If a key does not exist
    in the dict, yield the default value if specified, otherwise skip the
    missing key.  Afterwards, if ``other_keys`` is true, yield the remaining
    items in an arbitrary order.

    Usage::

        >>> dic = {"To": "you", "From": "me", "Date": "2008/1/4", "Subject": "X"}
        >>> dic["received"] = "..."
        >>> order = ["From", "To", "Subject"]
        >>> list(ordered_items(dic, order, False))
        [('From', 'me'), ('To', 'you'), ('Subject', 'X')]
    """
    d = dict(dic)
    for key in key_order:
        if key in d:
            yield key, d.pop(key)
        elif default is not NotGiven:
            yield key, default
    if other_keys:
        for key, value in d.iteritems():
            yield key, value

def del_keys(dic, *keys):
    """Delete several keys from a dict, ignoring those that don't exist.
    
    This modifies the dict in place.

    ::

        >>> d ={"A": 1, "B": 2, "C": 3}
        >>> del_keys(d, "A", "C")
        >>> d
        {'B': 2}
    """
    for key in keys:
        try:
            del dic[key]
        except KeyError:
            pass

def correlate_dicts(dicts, key):
    """Correlate several dicts under one superdict.

    If you have several dicts each with a 'name' key, this 
    puts them in a container dict keyed by name.

    Example::

        >>> d1 = {"name": "Fred", "age": 41}
        >>> d2 = {"name": "Barney", "age": 31}
        >>> flintstones = correlate_dicts([d1, d2], "name")
        >>> sorted(flintstones.keys())
        ['Barney', 'Fred']
        >>> flintstones["Fred"]["age"]
        41

    If you're having trouble spelling this method correctly, remember:
    "relate" has one 'l'.  The 'r' is doubled because it occurs after a prefix.
    Thus "correlate".
    """
    ret = {}
    i = 0
    for d in dicts:
        try:
            my_key = d[key]
        except KeyError:
            msg = "'dicts' element %d contains no key '%s'"
            tup = i, key 
            raise KeyError(msg % tup)
        ret[my_key] = d
        i += 1
    return ret



def correlate_objects(objects, attr):
    """Correlate several objects under one dict.

    If you have several objects each with a 'name' attribute, this
    puts them in a dict keyed by name.

    Example::

        >>> class Flintstone(DumbObject):
        ...    pass
        ...
        >>> fred = Flintstone(name="Fred", age=41)
        >>> barney = Flintstone(name="Barney", age=31)
        >>> flintstones = correlate_objects([fred, barney], "name")
        >>> sorted(flintstones.keys())
        ['Barney', 'Fred']
        >>> flintstones["Barney"].age
        31

    If you're having trouble spelling this method correctly, remember:
    "relate" has one 'l'.  The 'r' is doubled because it occurs after a prefix.
    Thus "correlate".
    """
    ret = {}
    i = 0
    for obj in objects:
        try:
            my_key = getattr(obj, attr)
        except AttributeError:
            msg = "'%s' object at 'objects[%d]' contains no attribute '%s'"
            tup = type(obj).__name__, i, attr 
            raise AttributeError(msg % tup)
        ret[my_key] = obj
        i += 1
    return ret


def distribute(lis, columns, direction, fill=None):
    """Distribute a list into a N-column table (list of lists).

    ``lis`` is a list of values to distribute.

    ``columns`` is an int greater than 1, specifying the number of columns in
    the table.

    ``direction`` is a string beginning with "H" (horizontal) or "V"
    (vertical), case insensitive.  This affects how values are distributed in
    the table, as described below.

    ``fill`` is a value that will be placed in any remaining cells if the data
    runs out before the last row or column is completed.  This must be an 
    immutable value such as ``None`` , ``""``, 0, "&nbsp;", etc.  If you
    use a mutable value like ``[]`` and later change any cell containing the
    fill value, all other cells containing the fill value will also be changed.

    The return value is a list of lists, where each sublist represents a row in
    the table.
    ``table[0]`` is the first row.
    ``table[0][0]`` is the first column in the first row.
    ``table[0][1]`` is the second column in the first row.

    This can be displayed in an HTML table via the following Mako template:

    .. code-block:: html+mako

        <table>
        % for row in table:
          <tr>
        % for cell in row:
            <td>${cell}</td>
        % endfor   cell
          </tr>
        % endfor   row
        </table>

    In a horizontal table, each row is filled before going on to the next row.
    This is the same as dividing the list into chunks::

        >>> distribute([1, 2, 3, 4, 5, 6, 7, 8], 3, "H")
        [[1, 2, 3], [4, 5, 6], [7, 8, None]]

    In a vertical table, the first element of each sublist is filled before
    going on to the second element.  This is useful for displaying an
    alphabetical list in columns, or when the entire column will be placed in
    a single <td> with a <br /> between each element::

        >>> food = ["apple", "banana", "carrot", "daikon", "egg", "fish", "gelato", "honey"]
        >>> table = distribute(food, 3, "V", "")
        >>> table
        [['apple', 'daikon', 'gelato'], ['banana', 'egg', 'honey'], ['carrot', 'fish', '']]
        >>> for row in table:
        ...    for item in row:
        ...         print "%-9s" % item,
        ...    print "."   # To show where the line ends.
        ...
        apple     daikon    gelato    .
        banana    egg       honey     .
        carrot    fish                .

    Alternatives to this function include a NumPy matrix of objects.

    """
    if columns < 1:
        raise ValueError("arg 'columns' must be >= 1")
    dir = direction[0].upper()
    if dir == "H":   # Horizontal table (row-wise)
        table = []
        for i in range(0, len(lis), columns):
            row = lis[i:i+columns]
            row_len = len(row)
            if row_len < columns:
                extra = [fill] * (columns - row_len)
                row.extend(extra)
            table.append(row)
        return table
    elif dir == "V":  # Vertical table (column-wise)
        total = len(lis)
        rows, remainder = divmod(total, columns)
        if remainder:
            rows += 1
        table = [[fill] * columns for x in range(rows)]
        #print table
        for i, elm in enumerate(lis):
            col, row = divmod(i, rows)
            #print "i=%d, row=%d, col=%d, element=%r" % (i, row, col, elm)
            table[row][col] = elm
        return table
    else:
        raise ValueError("arg ``direction`` must start with 'H' or 'V'")

def transpose(array):
    """Turn a list of lists sideways, making columns into rows and vice-versa.

    ``array`` must be rectangular; i.e., all elements must be the same 
    length. Otherwise the behavior is undefined: you may get ``IndexError``
    or missing items.

    Examples::

        >>> transpose([["A", "B", "C"], ["D", "E", "F"]])
        [['A', 'D'], ['B', 'E'], ['C', 'F']]
        >>> transpose([["A", "B"], ["C", "D"], ["E", "F"]])
        [['A', 'C', 'E'], ['B', 'D', 'F']]
        >>> transpose([])
        []
        
    Here's a pictoral view of the first example::

       A B C    =>    A D
       D E F          B E
                      C F

    This can be used to turn an HTML table into a group of div columns. An HTML
    table is row major: it consists of several <tr> rows, each containing
    several <td> cells.  But a <div> layout consists of only one row, each
    containing an entire subarray. The <div>s have style "float:left", which
    makes them appear horizontally. The items within each <div> are placed in
    their own <div>'s or separated by <br />, which makes them appear
    vertically.  The point is that an HTML table is row major (``array[0]`` is
    the first row), while a group of div columns is column major (``array[0]``
    is the first column). ``transpose()`` can be used to switch between the
    two.
    """
    if not array:
        return []
    ret = []
    for c in range(len(array[0])):
        col = [row[c] for row in array]
        ret.append(col)
    return ret
