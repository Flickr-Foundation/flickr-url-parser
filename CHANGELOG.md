# CHANGELOG

## v1.10.0 - 2024-09-04

*   Add a new method `looks_like_flickr_photo_id` which tells you if a particular string looks like a Flickr photo ID, or not.
*   Rename `is_flickr_user_id` to `looks_like_flickr_user_id` to clarify that this function is a quick heuristic, and not a guarantee that a user ID exists.

## v1.9.0 - 2024-05-22

*   When parsing a URL which points to a single photo, return the `user_url` and `user_id` (if they can be deduced from the URL).

## v1.8.3 - 2024-04-30

*   Add a trailing slash to the `user_url` returned in album URLs. This more closely matches the URL structured used on Flickr.com.

## v1.8.2 - 2024-02-02

*   Throw a more informative TypeError if you pass a non-string value as ``url``.

## v1.8.1 - 2024-01-02

*   Add support for recognising video download URLs like `/video_download.gne?id=[ID]`.
*   Add support for recognising static video URLs like `https://live.staticflickr.com/video/…`.
*   Add support for recognising Flash player video URLs like `https://www.flickr.com/apps/video/stewart.swf?photo_id=…`.

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

    e.g. `https://www.flickr.com/photos/circled/\xE2\x91\xA0\xE2\x91\xA1\xE2\x91\xA2\x60\x20\x77\x69\x6C\x6C\x20\x6E\x6F\x20\x6C\x6F\x6E\x67\x65\x72\x20\x62\x65\x20\x72\x65\x74\x75\x72\x6E\x65\x64\x20\x61\x73\x20\x61\x20\x70\x6C\x61\x75\x73\x69\x62\x6C\x65\x20\x70\x68\x6F\x74\x6F\x20\x55\x52\x4C\x2E\x0A\x0A\x23\x23\x20\x76\x31\x2E\x31\x2E\x30\x20\x2D\x20\x32\x30\x32\x33\x2D\x31\x30\x2D\x31\x38\x0A\x0A\x2A\x20\x20\x20\x41\x64\x64\x20\x74\x68\x65\x20\x61\x62\x69\x6C\x69\x74\x79\x20\x74\x6F\x20\x72\x75\x6E\x20\x66\x6C\x69\x63\x6B\x72\x5F\x75\x72\x6C\x5F\x70\x61\x72\x73\x65\x72\x20\x66\x72\x6F\x6D\x20\x74\x68\x65\x20\x63\x6F\x6D\x6D\x61\x6E\x64\x20\x6C\x69\x6E\x65\x2E\x0A\x2A\x20\x20\x20\x52\x65\x6D\x6F\x76\x65\x20\x73\x6F\x6D\x65\x20\x75\x6E\x6E\x65\x63\x65\x73\x73\x61\x72\x79\x20\x64\x65\x70\x65\x6E\x64\x65\x6E\x63\x69\x65\x73\x20\x66\x72\x6F\x6D\x20\x60\x73\x65\x74\x75\x70\x2E\x70\x79\x60\x2E\x0A\x0A\x23\x23\x20\x76\x31\x2E\x30\x2E\x30\x20\x2D\x20\x32\x30\x32\x33\x2D\x31\x30\x2D\x31\x37\x0A\x0A\x49\x6E\x69\x74\x69\x61\x6C\x20\x72\x65\x6C\x65\x61\x73\x65\x20\x6F\x66\x20\x74\x68\x69\x73\x20\x63\x6F\x64\x65\x20\x61\x73\x20\x61\x20\x73\x74\x61\x6E\x64\x61\x6C\x6F\x6E\x65\x20\x6C\x69\x62\x72\x61\x72\x79\x2E\x0A