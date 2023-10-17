import re

import httpx
import hyperlink

from flickr_url_parser.base58 import is_base58, base58_decode


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


def is_page(path_component):
    return re.match(r"^page\d+$", path_component)


def parse_flickr_url(url: str):
    """
    Categorises a Flickr URL, e.g. whether it's a single photo, an album,
    a user.

    This is the first step of flinumeration.
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
    if not url.startswith("http") and u.path[0].lower() in {
        "www.flickr.com",
        "flickr.com",
        "flic.kr",
    }:
        u = hyperlink.URL.from_text("https://" + url.rstrip("/"))

    # If this URL doesn't come from Flickr.com, then we can't possibly classify
    # it as a Flickr URL!
    is_long_url = u.host.lower() in {"www.flickr.com", "flickr.com"}
    is_short_url = u.host == "flic.kr"

    if not is_long_url and not is_short_url:
        raise NotAFlickrUrl(url)

    # This is for short URLs that point to:
    #
    #     - albums, e.g. http://flic.kr/s/aHsjybZ5ZD
    #     - galleries, e.g. https://flic.kr/y/2Xry4Jt
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

    # The URL for a single photo, e.g.
    # https://www.flickr.com/photos/coast_guard/32812033543/
    if (
        is_long_url
        and len(u.path) >= 3
        and u.path[0] == "photos"
        and u.path[2].isnumeric()
    ):
        return {
            "type": "single_photo",
            "photo_id": u.path[2],
        }

    # The URL for a single photo, e.g.
    #
    #     https://flic.kr/p/2p4QbKN
    #
    # Here the photo ID is a base-58 conversion of the photo ID.
    # See https://www.flickr.com/groups/51035612836@N01/discuss/72157616713786392/
    if is_short_url and len(u.path) == 2 and u.path[0] == "p" and is_base58(u.path[1]):
        return {"type": "single_photo", "photo_id": base58_decode(u.path[1])}

    # The URL for an album, e.g.
    #
    #     https://www.flickr.com/photos/cat_tac/albums/72157666833379009
    #     https://www.flickr.com/photos/cat_tac/sets/72157666833379009
    #
    if (
        is_long_url
        and len(u.path) == 4
        and u.path[0] == "photos"
        and u.path[2] in {"albums", "sets"}
        and u.path[3].isnumeric()
    ):
        return {
            "type": "album",
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
            "album_id": u.path[3],
        }

    # The URL for a user, e.g.
    #
    #     https://www.flickr.com/photos/blueminds/
    #     https://www.flickr.com/people/blueminds/
    #     https://www.flickr.com/photos/blueminds/albums
    #     https://www.flickr.com/people/blueminds/page3
    #
    if is_long_url and len(u.path) == 2 and u.path[0] in ("photos", "people"):
        return {
            "type": "user",
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
        }

    if (
        is_long_url
        and len(u.path) == 3
        and u.path[0] == "photos"
        and u.path[2] == "albums"
    ):
        return {
            "type": "user",
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
        }

    if (
        is_long_url
        and len(u.path) == 3
        and u.path[0] == "photos"
        and is_page(u.path[2])
    ):
        return {
            "type": "user",
            "user_url": f"https://www.flickr.com/photos/{u.path[1]}",
        }

    # URLs for a group, e.g.
    #
    #     https://www.flickr.com/groups/slovenia/pool
    #     https://www.flickr.com/groups/slovenia
    #     https://www.flickr.com/groups/slovenia/pool/page16
    #
    if is_long_url and len(u.path) == 2 and u.path[0] == "groups":
        return {
            "type": "group",
            "group_url": f"https://www.flickr.com/groups/{u.path[1]}",
        }

    if (
        is_long_url
        and len(u.path) == 3
        and u.path[0] == "groups"
        and u.path[2] == "pool"
    ):
        return {
            "type": "group",
            "group_url": f"https://www.flickr.com/groups/{u.path[1]}",
        }

    if (
        is_long_url
        and len(u.path) == 4
        and u.path[0] == "groups"
        and u.path[2] == "pool"
        and is_page(u.path[3])
    ):
        return {
            "type": "group",
            "group_url": f"https://www.flickr.com/groups/{u.path[1]}",
        }

    # URLs for a gallery, e.g.
    #
    #     https://www.flickr.com/photos/flickr/galleries/72157722096057728/
    #     https://www.flickr.com/photos/flickr/galleries/72157722096057728/page2
    #
    if (
        is_long_url
        and len(u.path) == 4
        and u.path[0] == "photos"
        and u.path[2] == "galleries"
        and u.path[3].isnumeric()
    ):
        return {"type": "galleries", "gallery_id": u.path[3]}

    if (
        is_long_url
        and len(u.path) == 5
        and u.path[0] == "photos"
        and u.path[2] == "galleries"
        and u.path[3].isnumeric()
        and is_page(u.path[4])
    ):
        return {"type": "galleries", "gallery_id": u.path[3]}

    # URL for a tag, e.g.
    #
    #     https://flickr.com/photos/tags/tennis/
    #     https://flickr.com/photos/tags/fluorspar/page1
    #
    if (
        is_long_url
        and len(u.path) == 3
        and u.path[0] == "photos"
        and u.path[1] == "tags"
    ):
        return {"type": "tags", "tag": u.path[2]}

    if (
        is_long_url
        and len(u.path) == 4
        and u.path[0] == "photos"
        and u.path[1] == "tags"
        and is_page(u.path[3])
    ):
        return {"type": "tags", "tag": u.path[2]}

    raise UnrecognisedUrl(f"Unrecognised URL: {url}")


__all__ = ['parse_flickr_url', 'UnrecognisedUrl', 'NotAFlickrUrl']
