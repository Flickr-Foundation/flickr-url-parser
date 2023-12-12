import re

import httpx
import hyperlink

from flickr_url_parser.base58 import is_base58, base58_decode
from flickr_url_parser._types import ParseResult

__version__ = "1.5.3"


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


def get_page(url: hyperlink.URL) -> int:
    """
    Flickr does pagination by appending a `pageXX` component to the end of URLs, e.g.

        https://www.flickr.com/photos/belindavick/
        https://www.flickr.com/photos/belindavick/page2
        https://www.flickr.com/photos/belindavick/page3

    This returns the page number for a path component.  It assumes that this is
    a valid pagination parameter.

        >>> get_page('https://www.flickr.com/photos/belindavick/')
        1

        >>> get_page('https://www.flickr.com/photos/belindavick/page3')
        3

    """
    assert len(url.path) >= 1
    final_component = url.path[-1]

    m = re.match(r"^page([0-9]+)$", final_component)

    if m is not None:
        return int(m.group(1))
    else:
        return 1


def is_page(path_component: str) -> bool:
    """
    Returns True if a path component looks like pagination in a Flickr URL,
    False otherwise.
    """
    return re.match(r"^page[0-9]+$", path_component) is not None


def is_digits(path_component: str) -> bool:
    """
    Returns True if ``path_component`` is a non-empty string of
    digits 0-9, False otherwise.

    Note: this is different from ``str.isdigit()`` or ``str.isnumeric()``,
    both of which admit a wider range of characters that we wouldn't
    expect to see in a Flickr URL.

        >>> '①'.isdigit()
        True
        >>> '½'.isnumeric()
        True

    """
    return re.match(r"^[0-9]+$", path_component) is not None


def parse_flickr_url(url: str) -> ParseResult:
    """
    Parse a Flickr URL and return some key information, e.g. whether it's
    a single photo, an album, a user.

    The return value will be a dictionary with a key ``type`` and then some
    extra keys depending on the type, e.g.

        {"type": "single_photo", "photo_id": "50567413447"}

    Possible values for ``type``:

    -   ``single_photo``
            This will include a single extra key: ``photo_id``.

    -   ``album``
            This will include two extra keys: ``album_id`` and ``user_url``.
            Look up the latter with Flickr's ``flickr.urls.lookupUser`` API.

    -   ``user``
            This will include a single extra key: ``user_url``.
            Look up the latter with Flickr's ``flickr.urls.lookupUser`` API.

    -   ``group``
            This will include a single extra key: ``group_url``.
            Look it up with Flickr's ``flickr.urls.lookupGroup`` API.

    -   ``gallery``
            This will include a single extra key: ``gallery_id``.

    -   ``tag``
            This will include a single extra key: ``tag``.

    If you pass a URL which isn't a Flickr URL, or a Flickr URL which
    isn't recognised, then the function will throw ``NotAFlickrUrl``
    or ``UnrecognisedUrl`` exceptions.

    """
    try:
        u = hyperlink.URL.from_text(url.rstrip("/"))

    # This is for anything which any string can't be parsed as a URL,
    # e.g. `https://https://`
    #
    # Arguably some of those might be malformed URLs from flickr.com,
    # but it's a rare enough edge case that this is fine.
    except hyperlink.URLParseError:
        raise NotAFlickrUrl(url)

    # Handle URLs without a scheme, e.g.
    #
    #     flickr.com/photos/1234
    #
    # We know what the user means, but the hyperlink URL parsing library
    # thinks this is just the path component, not a sans-HTTP URL.
    #
    # These lines convert this to a full HTTPS URL, i.e.
    #
    #     https://flickr.com/photos/1234
    #
    # which allows the rest of the logic in the function to do
    # the "right thing" with this URL.
    if not url.startswith("http"):
        if u.path[0].lower() in {
            "www.flickr.com",
            "flickr.com",
            "flic.kr",
            "live.staticflickr.com",
        }:
            u = hyperlink.URL.from_text("https://" + url.rstrip("/"))

        if (
            u.path
            and re.match(r"^photos[0-9]+\.flickr\.com$", u.path[0].lower()) is not None
        ):
            u = hyperlink.URL.from_text("https://" + url.rstrip("/"))

        if (
            u.path
            and re.match(r"^farm[0-9]+\.static\.flickr\.com$", u.path[0].lower())
            is not None
        ):
            u = hyperlink.URL.from_text("https://" + url.rstrip("/"))

    # If this URL doesn't come from Flickr.com, then we can't possibly classify
    # it as a Flickr URL!
    is_long_url = u.host.lower() in {"www.flickr.com", "flickr.com"}
    is_short_url = u.host == "flic.kr"
    is_static_url = (
        u.host == "live.staticflickr.com"
        or re.match(r"^photos[0-9]+\.flickr\.com$", u.host) is not None
        or re.match(r"^farm[0-9]+\.static\.flickr\.com$", u.host) is not None
    )

    if not is_long_url and not is_short_url and not is_static_url:
        raise NotAFlickrUrl(url)

    # This is for short URLs that point to:
    #
    #     - albums, e.g. http://flic.kr/s/aHsjybZ5ZD
    #     - gallery, e.g. https://flic.kr/y/2Xry4Jt
    #     - people/users, e.g. https://flic.kr/ps/ZVcni
    #
    # Although we can base58 decode the album ID, that doesn't tell
    # us the user URL -- it goes to an intermediary "short URL" service,
    # and there's no obvious way in the API to go album ID -> user.
    if (
        is_short_url
        and len(u.path) == 2
        and u.path[0] in {"s", "y", "ps"}
        and is_base58(u.path[1])
    ):
        try:
            redirected_url = str(httpx.get(url, follow_redirects=True).url)
            assert redirected_url != url
            return parse_flickr_url(redirected_url)
        except Exception as e:
            print(e)
            pass

    # This is for "guest pass" URLs that point to:
    #
    #     - albums, e.g. https://www.flickr.com/gp/realphotomatt/M195SLkj98
    #       (from https://twitter.com/PAPhotoMatt/status/1715111983974940683)
    #     - single photos, e.g.
    #       https://www.flickr.com/gp/199246608@N02/nSN80jZ64E
    #       (this is one of mine)
    #
    # See https://www.flickrhelp.com/hc/en-us/articles/4404069601172-Create-or-delete-temporary-Guest-Passes-in-Flickr
    #
    # I don't think these guest pass URLs are deterministic -- they don't
    # contain base58 encoded IDs (notice that `nSN80jZ64E` has a `0`) and
    # the user can revoke them later.
    #
    # The easiest thing to do is to do an HTTP lookup.
    if is_long_url and len(u.path) > 1 and u.path[0] == "gp":
        try:
            redirected_url = str(httpx.get(url, follow_redirects=True).url)
            assert redirected_url != url
            return parse_flickr_url(redirected_url)
        except Exception as e:
            print(e)
            pass

    # The URL for a single photo, e.g.
    # https://www.flickr.com/photos/coast_guard/32812033543/
    if (
        is_long_url
        and len(u.path) >= 3
        and u.path[0] == "photos"
        and is_digits(u.path[2])
    ):
        return {
            "type": "single_photo",
            "photo_id": u.path[2],
        }

    # Old-style URLs for a single photo, e.g.
    # http://flickr.com/photo/17277074@N00/2619974961
    #
    # This is a variant of Flickr photo URL that appears fairly
    # regularly in e.g. Wikimedia Commons – it no longer resolves, but
    # there are enough of these both on WMC and around the general web
    # that I think this was once a supported URL format.
    #
    # It's clear enough what this means that we should be able to
    # parse it, even if new URLs like this are no longer created.
    if (
        is_long_url
        and len(u.path) >= 3
        and u.path[0] == "photo"
        and is_digits(u.path[2])
    ):
        return {
            "type": "single_photo",
            "photo_id": u.path[2],
        }

    # The URL for a single photo, e.g.
    #
    #     https://flic.kr/p/2p4QbKN
    #
    # Here the final path component is a base-58 conversion of the photo ID.
    # See https://www.flickr.com/groups/51035612836@N01/discuss/72157616713786392/
    if is_short_url and len(u.path) == 2 and u.path[0] == "p" and is_base58(u.path[1]):
        return {"type": "single_photo", "photo_id": base58_decode(u.path[1])}

    # Another variant of URL for a single photo, e.g.
    #
    #     https://www.flickr.com/photo_zoom.gne?id=196155401&size=m
    #     https://www.flickr.com/photo_exif.gne?id=1427904898
    #
    # Today this redirects to the /sizes/ or the /meta/ page, but it's quite
    # commonly used in e.g. Wikimedia Commons.
    if (
        is_long_url
        and (u.path == ("photo_zoom.gne",) or u.path == ("photo_exif.gne",))
        and len(u.get("id")) == 1
    ):
        photo_id = u.get("id")[0]

        if isinstance(photo_id, str) and is_digits(photo_id):
            return {"type": "single_photo", "photo_id": photo_id}

    # The URL for an actual file, e.g.
    #
    #     https://live.staticflickr.com/65535/53381630964_63d765ee92_s.jpg
    #     https://photos12.flickr.com/16159487_3a6615a565_b.jpg
    #     http://farm1.static.flickr.com/82/241708183_dd0847d5c7_o.jpg
    #
    # The exact format of these URLs is described in the Flickr docs:
    # https://www.flickr.com/services/api/misc.urls.html
    if is_static_url:
        if u.host == "live.staticflickr.com" and is_digits(u.path[0]):
            photo_id, *_ = u.path[1].split("_")
            if is_digits(photo_id):
                return {"type": "single_photo", "photo_id": photo_id}

        if re.match(r"^photos\d+\.flickr\.com$", u.host) and len(u.path) >= 1:
            photo_id, *_ = u.path[0].split("_")
            if is_digits(photo_id):
                return {"type": "single_photo", "photo_id": photo_id}

        if re.match(r"^farm\d+\.static\.flickr\.com$", u.host) and is_digits(u.path[0]):
            photo_id, *_ = u.path[1].split("_")
            if is_digits(photo_id):
                return {"type": "single_photo", "photo_id": photo_id}

    # The URL for an album, e.g.
    #
    #     https://www.flickr.com/photos/cat_tac/albums/72157666833379009
    #     https://www.flickr.com/photos/cat_tac/sets/72157666833379009
    #     https://www.flickr.com/photos/andygocher/albums/72157648252420622/page3
    #
    if (
        is_long_url
        and 4 <= len(u.path) <= 5
        and u.path[0] == "photos"
        and u.path[2] in {"albums", "sets"}
        and is_digits(u.path[3])
    ):
        return {
            "type": "album",
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
            "album_id": u.path[3],
            "page": get_page(u),
        }

    # The URL for a user, e.g.
    #
    #     https://www.flickr.com/photos/blueminds/
    #     https://www.flickr.com/people/blueminds/
    #     https://www.flickr.com/photos/blueminds/albums
    #     https://www.flickr.com/people/blueminds/page3
    #
    if is_long_url and len(u.path) >= 2 and u.path[0] in {"photos", "people"}:
        user_url = f"https://www.flickr.com/photos/{u.path[1]}"

        if len(u.path) == 2:
            return {"type": "user", "user_url": user_url, "page": 1}

        if len(u.path) == 3 and u.path[0] == "photos" and u.path[2] == "albums":
            return {"type": "user", "user_url": user_url, "page": 1}

        if len(u.path) == 3 and u.path[0] == "photos" and is_page(u.path[2]):
            return {
                "type": "user",
                "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
                "page": get_page(u),
            }

    # URLs for a group, e.g.
    #
    #     https://www.flickr.com/groups/slovenia/pool
    #     https://www.flickr.com/groups/slovenia
    #     https://www.flickr.com/groups/slovenia/pool/page16
    #
    if is_long_url and len(u.path) >= 2 and u.path[0] == "groups":
        if len(u.path) == 2:
            return {
                "type": "group",
                "group_url": f"https://www.flickr.com/groups/{u.path[1]}",
                "page": 1,
            }

        if u.path[2] == "pool":
            return {
                "type": "group",
                "group_url": f"https://www.flickr.com/groups/{u.path[1]}",
                "page": get_page(u),
            }

    # URLs for a gallery, e.g.
    #
    #     https://www.flickr.com/photos/flickr/gallery/72157722096057728/
    #     https://www.flickr.com/photos/flickr/gallery/72157722096057728/page2
    #     https://www.flickr.com/photos/flickr/galleries/72157690638331410/
    #
    if (
        is_long_url
        and len(u.path) >= 4
        and u.path[0] == "photos"
        and u.path[2] in {"gallery", "galleries"}
        and is_digits(u.path[3])
    ):
        return {"type": "gallery", "gallery_id": u.path[3], "page": get_page(u)}

    # URL for a tag, e.g.
    #
    #     https://flickr.com/photos/tags/tennis/
    #     https://flickr.com/photos/tags/fluorspar/page1
    #
    if (
        is_long_url
        and len(u.path) >= 3
        and u.path[0] == "photos"
        and u.path[1] == "tags"
    ):
        return {"type": "tag", "tag": u.path[2], "page": get_page(u)}

    raise UnrecognisedUrl(f"Unrecognised URL: {url}")


__all__ = ["parse_flickr_url", "UnrecognisedUrl", "NotAFlickrUrl", "ParseResult"]
