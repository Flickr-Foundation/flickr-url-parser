# CHANGELOG

## v1.8.0 - 2023-12-27

*   Add an optional `id` parameter to the `User` type.

    If you parse the URL for a user's photostream and use the URL that contains their NSID rather than their path alias, this ID will be included in the response.
    This allows for slightly faster lookups later.

## v1.7.1 - 2023-12-20

*   Add support for recognising URLs that use `/photo_edit.gne?id=[ID]` and `/photo.gne?short=[SHORT_ID]`.

## v1.7.0 - 2023-12-17

Add support for recognising URLs as the Flickr homepage.

There are lots of varieties of homepage URL that appear in e.g. links from Wikimedia Commons, and now they can be recognised:

```pycon
>>> parse_flickr_url("www.flickr.com")
{"type": "homepage"}
```

## v1.6.1 - 2023-12-15

*   Fix a bug where the URL parser could throw an IndexError on URL fragments or empty strings.

## v1.6.0 - 2023-12-12

*   Add a new function `find_flickr_urls_in_text` which can be used to find Flickr URLs in a block of arbitrary text.
    Example:
    
    ```pycon
    >>> text = """
    ... This is the help page: https://www.flickr.com/help
    ...
    ... This is a user: https://www.flickr.com/photos/mariakallin/
    ... """
    >>> find_flickr_urls_in_text(text)
    ['https://www.flickr.com/help', 'https://www.flickr.com/photos/mariakallin/']
    ```
    
    This is useful for text analysis.

## v1.5.3 - 2023-12-12

Add support for parsing more varieties of URL, based on those seen in the Wikimedia Commons snapshots, including:

*   Old-style photo URLs that use `/photo/` instead of `/photos/`, e.g. `http://flickr.com/photo/17277074@N00/2619974961`
*   Photo URLs that use the `/photo_zoom.gne` path and similar `.gne` paths, e.g. `https://www.flickr.com/photo_zoom.gne?id=196155401&size=m`
*   A wide variety of `static.flickr.com`-like URLs; URLs that point to raw JPEGs rather than the photo description page

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
