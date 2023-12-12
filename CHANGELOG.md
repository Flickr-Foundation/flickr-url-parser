# CHANGELOG

## v1.5.2 - 2023-12-12

*   Expand the support for parsing static URLs, e.g. `http://farm1.static.flickr.com/82/241abc183_dd0847d5c7_o.jpg`

## v1.5.1 - 2023-12-08

*   Expand the support for parsing static URLs, e.g. `https://photos12.flickr.com/16159487_3a6615a565_b.jpg`

## v1.5.0 - 2023-12-07

*   Add support for parsing static URLs, e.g. `https://live.staticflickr.com/65535/53381630964_63d765ee92_s.jpg`

## v1.4.0 - 2023-12-02

*   Drop support for Python 3.7 to Python 3.11; this library now requires Python 3.12.

## v1.3.0 - 2023-11-09

*   Add support for pagination.  All collection URLs (albums, users, groups, galleries and tags) now include a `page` parameter that tells you what page you've navigated to in the Flickr UI.

## v1.2.4 - 2023-11-05

*   Explicitly export the `ParseResult` type.

## v1.2.3 - 2023-11-05

*   Actually make the type hints available by adding the `py.typed` file.

## v1.2.2 - 2023-10-31

*   Add type hints that can be used for type checking with mypy and similar tools.

## v1.2.1 - 2023-10-23

*   Add support for Flickr Guest Pass URLs, e.g. `https://www.flickr.com/gp/realphotomatt/M195SLkj98`

## v1.1.1 - 2023-10-20

*   Tighten up the definition of "numeric ID" in Flickr URLs, so only something that could plausibly be a numeric ID is allowed.

    e.g. `https://www.flickr.com/photos/circled/①②③` will no longer be returned as a plausible photo URL.

## v1.1.0 - 2023-10-18

*   Add the ability to run flickr_url_parser from the command line.
*   Remove some unnecessary dependencies from `setup.py`.

## v1.0.0 - 2023-10-17

Initial release of this code as a standalone library.
