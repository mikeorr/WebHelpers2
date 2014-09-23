"""Number formatting, numeric helpers, and numeric statistics."""

import math
import re

#### Calculations ####

def percent_of(part, whole):
    """What percent of ``whole`` is ``part``?
    """
    # Use float to force true division.
    return float(part * 100) / whole

#### Statistics ####

def mean(r):
    """Return the mean (i.e., average) of a sequence of numbers.
    """
    try:
        return float(sum(r)) / len(r)
    except ZeroDivisionError:
        raise ValueError("can't calculate mean of empty collection")

average = mean

def median(r):
    """Return the median of an iterable of numbers.

    The median is the point at which half the numbers are lower than it and
    half the numbers are higher.  This gives a better sense of the majority
    level than the mean (average) does, because the mean can be skewed by a few
    extreme numbers at either end.  For instance, say you want to calculate
    the typical household income in a community and you've sampled four
    households:

    >>> incomes = [18000]       # Fast food crew
    >>> incomes.append(24000)   # Janitor
    >>> incomes.append(32000)   # Journeyman
    >>> incomes.append(44000)   # Experienced journeyman
    >>> incomes.append(67000)   # Manager
    >>> incomes.append(9999999) # Bill Gates
    >>> median(incomes)
    38000.0
    >>> mean(incomes)
    1697499.8333333333

    The median here is somewhat close to the majority of incomes, while the
    mean is far from anybody's income.
    
    This implementation makes a temporary list of all numbers in memory.
    """
    s = list(r)
    s_len = len(s)
    if s_len == 0:
        raise ValueError("can't calculate median of empty collection")
    s.sort()
    center = s_len // 2
    is_odd = s_len % 2
    if is_odd:
        return s[center]   # Return the center element.
    # Return the average of the two elements nearest the center.
    low = s[center-1]
    high = s[center]
    return mean([low, high])

def standard_deviation(r, sample=True):
    """Standard deviation. 
    
    `From the Python Cookbook
    <http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/442412>`_.
    Population mode contributed by Lorenzo Catucci.

    Standard deviation shows the variability within a sequence of numbers.
    A small standard deviation means the numbers are close to each other.  A
    large standard deviation shows they are widely different.  In fact it
    shows how far the numbers tend to deviate from the average.  This can be
    used to detect whether the average has been skewed by a few extremely high
    or extremely low values.

    Most natural and random phenomena follow the normal distribution (aka the
    bell curve), which says that most values are close to average but a few are
    extreme.  E.g., most people are close to 5'9" tall but a few are very tall
    or very short.  If the data does follow the bell curve, 68% of the values
    will be within 1 standard deviation (stdev) of the average, and 95% will be
    within 2 standard deviations.  So a university professor grading exams on a
    curve might give a "C" (mediocre) grade to students within 1 stdev of the
    average score, "B" (better than average) to those within 2 stdevs above,
    and "A" (perfect) to the 0.25% higher than 2 stdevs.  Those between 1 and 2
    stdevs below get a "D" (poor), and those below 2 stdevs... we won't talk
    about them.

    By default the helper computes the unbiased estimate
    for the population standard deviation, by applying an unbiasing
    factor of sqrt(N/(N-1)).

    If you'd rather have the function compute the population standard
    deviation, pass ``sample=False``.

    The following examples are taken from Wikipedia.
    http://en.wikipedia.org/wiki/Standard_deviation

        >>> standard_deviation([0, 0, 14, 14])
        8.082903768654761...
        >>> standard_deviation([0, 6, 8, 14])
        5.773502691896258...
        >>> standard_deviation([6, 6, 8, 8])
        1.1547005383792515
        >>> standard_deviation([0, 0, 14, 14], sample=False)
        7.0
        >>> standard_deviation([0, 6, 8, 14], sample=False)
        5.0
        >>> standard_deviation([6, 6, 8, 8], sample=False)
        1.0

    (The results reported in Wikipedia are those expected for whole
    population statistics and therefore are equal to the ones we get
    by setting ``sample=False`` in the later tests.)
    
    .. code-block:: pycon
    
        # Fictitious average monthly temperatures in Southern California.
        #                       Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
        >>> standard_deviation([70, 70, 70, 75, 80, 85, 90, 95, 90, 80, 75, 70])
        9.003366373785...
        >>> standard_deviation([70, 70, 70, 75, 80, 85, 90, 95, 90, 80, 75, 70], sample=False)
        8.620067027323...

        # Fictitious average monthly temperatures in Montana.
        #                       Jan  Feb  Mar Apr May Jun Jul  Aug Sep Oct Nov Dec
        >>> standard_deviation([-32, -10, 20, 30, 60, 90, 100, 80, 60, 30, 10, -32])
        45.1378360405574...
        >>> standard_deviation([-32, -10, 20, 30, 60, 90, 100, 80, 60, 30, 10, -32], sample=False) # doctest: +ELLIPSIS
        43.2161878106906...
    """
    avg = average(r)
    sdsq = sum([(i - avg) ** 2 for i in r])
    if sample:
        normal_denom=len(r) - 1 or 1
    else:
        normal_denom=len(r)
    return (sdsq / normal_denom) ** 0.5


#### Number formatting ####

def format_data_size(size, unit, precision=1, binary=False, full_name=False):
    """Format a number using SI units (kilo, mega, etc.).

    ``size``: The number as a float or int.

    ``unit``: The unit name in plural form. Examples: "bytes", "B".

    ``precision``: How many digits to the right of the decimal point. Default
    is 1.  0 suppresses the decimal point.

    ``binary``: If false, use base-10 decimal prefixes (kilo = K = 1000).  
    If true, use base-2 binary prefixes (kibi = Ki = 1024).  

    ``full_name``: If false (default), use the prefix abbreviation ("k" or
    "Ki").  If true, use the full prefix ("kilo" or "kibi"). If false,
    use abbreviation ("k" or "Ki").

    Examples:

    >>> format_data_size(1024, "B")
    '1.0 kB'
    >>> format_data_size(1024, "B", 2)
    '1.02 kB'
    >>> format_data_size(1024, "B", 2, binary=True)
    '1.00 KiB'
    >>> format_data_size(54000, "Wh", 0)
    '54 kWh'
    >>> format_data_size(85000, "m/h", 0)
    '85 km/h'
    >>> format_data_size(85000, "m/h", 0).replace("km/h", "klicks")
    '85 klicks'
    """
    # Contributed by Wojciech Malinowski
    if full_name is None:
        full_name = len(unit) > 1
        
    if not binary:
        base = 1000
        if full_name:
            multiples = ('', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa', 'zetta', 'yotta')
        else:
            multiples = ('', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    else:
        base = 1024
        if full_name:
            multiples = ('', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi', 'zebi', 'yobi')
        else:
            multiples = ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi')
            
    if size <= 0:
        m = 0
    else:
        m = int(math.log(size) / math.log(base))
    if m > 8:
        m = 8

    if m == 0:
        precision = '%.0f'
    else:
        precision = '%%.%df' % precision
        
    size = precision % (size / math.pow(base, m))

    return '%s %s%s' % (size.strip(), multiples[m], unit)

def format_byte_size(size, precision=1, binary=False, full_name=False):
    """Same as ``format_data_size`` but specifically for bytes.
    
    Examples:

    >>> format_byte_size(2048)
    '2.0 kB'
    >>> format_byte_size(2048, full_name=True)
    '2.0 kilobytes'
    """
    if full_name:
        return format_data_size(size, "bytes", precision, binary, True)
    else:
        return format_data_size(size, "B", precision, binary, False)

def format_bit_size(size, precision=1, binary=False, full_name=False):
    """Same as ``format_data_size`` but specifically for bits.

    Examples:

    >>> format_bit_size(2048)
    '2.0 kb'
    >>> format_bit_size(2048, full_name=True)
    '2.0 kilobits'
    """
    if full_name:
        return format_data_size(size, "bits", precision, binary, True)
    else:
        return format_data_size(size, "b", precision, binary, False)
