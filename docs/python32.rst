Python 3.2 Caveats
%%%%%%%%%%%%%%%%%%

On Python 3.2 you'll have to use MarkupSafe_ 0.15. Version 0.16 started
using the "u" string prefix which is invalid in Python 3.0 - 3.2. (It was
re-added in 3.3.)

WebHelpers2 is believed to run on Python 3.2 but this has not yet been tested.
All "u" prefixes were removed from the code but remain in some former doctests.
(These are no longer supported as doctests but are usage examples.)


.. _markupsafe: http://pypi.python.org/pypi/markupsafe
