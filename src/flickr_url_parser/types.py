"""
Different types of parsed URL which might be returned by ``flickr_url_parser``.
"""

import typing


class Homepage(typing.TypedDict):
    """
    The Flickr.com homepage.
    """

    type: typing.Literal["homepage"]


class SinglePhoto(typing.TypedDict):
    """
    A single photo on Flickr.com.
    """

    type: typing.Literal["single_photo"]
    photo_id: str
    user_url: str | None
    user_id: str | None


def anonymous_single_photo(photo_id: str) -> SinglePhoto:
    """
    A single photo where only the photo ID is known, and nothing about
    the photo's owner.
    """
    return {
        "type": "single_photo",
        "photo_id": photo_id,
        "user_url": None,
        "user_id": None,
    }


class Album(typing.TypedDict):
    """
    An album on Flickr.com.

    An album is a collection of your own photos.  It can only contain
    photos that you uploaded.

    It's possible to paginate through large albums.
    """

    type: typing.Literal["album"]
    user_url: str
    album_id: str
    page: int


class User(typing.TypedDict):
    """
    A user's profile on Flickr.com.

    If you're looking at a user's photostream, it can be paginated.
    The ``page`` parameter is only returned if you're in this view.
    """

    type: typing.Literal["user"]
    page: int
    user_url: str
    user_id: str | None


class Group(typing.TypedDict):
    """
    A group on Flickr.com.

    A group is a collection of users who shared a common interest or focus,
    who put their photos in a shared "pool".  The pool may be paginated.
    """

    type: typing.Literal["group"]
    group_url: str
    page: int


class Gallery(typing.TypedDict):
    """
    A gallery on Flickr.com.

    A gallery is a collection of other people's photos.  It can only
    contain photos uploaded by other people.

    It's possible to paginate through large galleries.
    """

    type: typing.Literal["gallery"]
    gallery_id: str
    page: int


class Tag(typing.TypedDict):
    """
    A list of photos with a tag on Flickr.com.

    It's possible to paginate through popular tags.
    """

    type: typing.Literal["tag"]
    tag: str
    page: int


ParseResult = Homepage | SinglePhoto | Album | User | Group | Gallery | Tag
