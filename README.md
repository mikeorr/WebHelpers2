# WebHelpers2

WebHelpers2 provides functions useful in web applications: generating HTML tags,
showing results a pageful at a time, etc. It may be used with any web
framework or template engine. A brief outline is below, but see the
documentation and module docstrings for a more complete list.

Documentation is in the docs/ directory or read the [online documentation]([_online documentation]).
(It includes instructions on migrating from Webhelpers.)

## constants

Country codes, states and provinces.

## containers

High-level container objects and dict/list helpers.

## date

Date/time helpers. These currently format strings based on dates.

## html

A package of HTML-related helpers.

### builder

A library for generating HTML tags with smart escaping. All
public symbols are imported into ``webhelpers.html``.

### tags

High-level HTML tags, including form tags, hyperlinks, and
Javascript/CSS links. The ``ModelTags`` class builds input
tags from database records (for any kind of database).

### tools

Helpers producing chunks of HTML. Also test-to-HTML and HTML-to-text
converters.

## misc

Miscellaneous helpers that are neither text, numeric, container, or date.

## number

Numeric helpers and number formatters.

## text

Helpers producing string output, suitable for both HTML and non-HTML
applications.

For support/question/patches, please use the [Pylons mailing list]
(http://groups.google.com/group/pylons-discuss).

## Requirements

WebHelpers2 depends on [MarkupSafe][_MarkupSafe] and [six][_six], and it can also use [Unidecode][_unidecode] if
you have it installed.

## Contributing

To install
```bash
poetry install --with dev
```

To run tests
```bash
make check 
```

To package.
```bash
make build 
```

[_online documentation]: http://webhelpers2.readthedocs.org/en/latest/

[_MarkupSafe]: http://pypi.python.org/pypi/MarkupSafe

[_six]: http://pypi.python.org/pypi/six

[_unidecode]:  http://python.org/pypi/Unidecode/
