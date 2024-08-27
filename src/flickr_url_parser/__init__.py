"""
``flickr_url_parser`` is a library for parsing Flickr URLs.

You enter a Flickr URL, and it tells you what it points to --
a single photo, an album, a gallery, and so on.
"""

from .exceptions import NotAFlickrUrl, UnrecognisedUrl
from .matcher import find_flickr_urls_in_text
from .parser import is_flickr_user_id, parse_flickr_url
from .types import ParseResult

__version__ = "1.9.0"


__all__ = [
    "is_flickr_user_id",
    "find_flickr_urls_in_text",
    "parse_flickr_url",
    "UnrecognisedUrl",
    "NotAFlickrUrl",
    "ParseResult",
]
