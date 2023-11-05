# CHANGELOG

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
