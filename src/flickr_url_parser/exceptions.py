class NotAFlickrUrl(Exception):
    """
    Raised when somebody tries to flinumerate a URL which isn't from Flickr.
    """

    pass


class UnrecognisedUrl(Exception):
    """
    Raised when somebody tries to flinumerate a URL on Flickr, but we
    can't work out what photos are there.
    """

    pass
