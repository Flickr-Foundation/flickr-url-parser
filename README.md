# flickr-url-parser

This is a library for parsing Flickr URLs.
You enter a Flickr URL, and it tells you what it points to – a single photo, an album, a gallery, and so on.

Examples:

```console
$ flickr_url_parser "https://www.flickr.com/photos/sdasmarchives/50567413447"
{"type": "single_photo", "photo_id": "50567413447"}

$ flickr_url_parser "https://www.flickr.com/photos/aljazeeraenglish/albums/72157626164453131"
{"type": "album", "user_url": "https://www.flickr.com/photos/aljazeeraenglish", "album_id": "72157626164453131", "page": 1}

$ flickr_url_parser "https://www.flickr.com/photos/blueminds/page3"
{"type": "user", "user_url": "https://www.flickr.com/photos/blueminds"}
```

## Motivation

There's a lot of variety in Flickr URLs, even among URLs that point to the same thing.
For example, all four of these URLs point to the same photo:

```
https://www.flickr.com/photos/sdasmarchives/50567413447
http://flickr.com/photos/49487266@N07/50567413447
https://www.flickr.com/photo.gne?id=50567413447
https://live.staticflickr.com/65535/50567413447_afec74ef45_o_d.jpg
```

Dealing with all these variants can be tricky – this library aims to simplify that.
We use it for [Flinumeratr], [Flickypedia], and other [Flickr Foundation] projects.

[Flinumeratr]: https://www.flickr.org/tools/flinumeratr/
[Flickypedia]: https://www.flickr.org/tools/flickypedia/
[Flickr Foundation]: https://www.flickr.org/

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

If you want to make changes to the library, there are instructions in [CONTRIBUTING.md](./CONTRIBUTING.md).

## Useful reading

-   Photo Image URLs in the Flickr docs: <https://www.flickr.com/services/api/misc.urls.html>

## License

This project is dual-licensed as Apache-2.0 and MIT.
