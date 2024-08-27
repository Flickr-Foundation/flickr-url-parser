"""
Exceptions that are thrown when we're unable to parse a URL as
a Flickr URL.
"""


class NotAFlickrUrl(Exception):
    """
    Raised when somebody tries to parse a URL which isn't from Flickr.
    """

    pass


class UnrecognisedUrl(Exception):
    """
    Raised when somebody tries to parse a URL on Flickr, but we
    can't work out what photos are there.
    """

    pass
