# flickr-url-parser

This is a library for parsing Flickr URLs.
You enter a Flickr URL, and it tells you what sort of URL it is.

Examples:

```console
$ flickr_url_parser "https://www.flickr.com/photos/sdasmarchives/50567413447"
{"type": "single_photo", "photo_id": "50567413447"}

$ flickr_url_parser "https://www.flickr.com/photos/aljazeeraenglish/albums/72157626164453131"
{"type": "album", "user_url": "https://www.flickr.com/photos/aljazeeraenglish", "album_id": "72157626164453131"}

$ flickr_url_parser "https://www.flickr.com/people/blueminds/"
{"type": "user", "user_url": "https://www.flickr.com/photos/blueminds"}
```

This was extracted as a standalone bit of functionality from [Flinumeratr], a toy that shows you a list of photos that can be viewed at a Flickr URL.

[Flinumeratr]: https://github.com/flickr-foundation/flinumeratr

## Usage

There are two ways to use flickr_url_parser:

1.  **As a command-line tool.**
    Run `flickr_url_parser`, passing the Flickr URL as a single argument:
    
    ```console
    $ flickr_url_parser "https://www.flickr.com/photos/sdasmarchives/50567413447"
    {"type": "single_photo", "photo_id": "50567413447"}
    ```
    
    The result will be printed as a JSON object.
    
    To see more information about the possible return values, run `flickr_url_parser --help`.

2.  **As a Python library.**
    Import the function `parse_flickr_url` and pass the Flickr URL as a single argument:

    ```pycon
    >>> from flickr_url_parser import parse_flickr_url

    >>> parse_flickr_url("https://www.flickr.com/photos/sdasmarchives/50567413447")
    {"type": "single_photo", "photo_id": "50567413447"}
    ```
    
    To see more information about the possible return values, use the [`help` function](https://docs.python.org/3/library/functions.html#help):
    
    ```pycon
    >>> help(parse_flickr_url)
    ```

Note that just because a URL can be parsed does not mean it can be *resolved* to a photo and/or photos.
The only way to know if there are photos behind the URL is to (1) try to fetch the URL or (2) use the output from the parser to ask the Flickr API for photos.

## Development

You can set up a local development environment by cloning the repo and installing dependencies:

```console
$ git clone https://github.com/Flickr-Foundation/flickr-url-parser.git
$ cd flickr-url-parser
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -e .
```

If you want to run tests, install the dev dependencies and run py.test:

```console
$ source .venv/bin/activate
$ pip install -r dev_requirements.txt
$ coverage run -m pytest tests
$ coverage report
```

To create a new version on PyPI:

1.  Update the version in `src/flickr_url_parser/__init__.py`
2.  Add release notes in `CHANGELOG.md` and push a new tag to GitHub
3.  Deploy the release using twine:

    ```console
    $ python3 setup.py sdist
    $ python3 -m twine upload dist/* --username=__token__
    ```
    
    You will need [a PyPI API token](https://pypi.org/help/#apitoken) to publish packages.

## Useful reading

-   Photo Image URLs in the Flickr docs: <https://www.flickr.com/services/api/misc.urls.html>

## License

This project is dual-licensed as Apache-2.0 and MIT.
