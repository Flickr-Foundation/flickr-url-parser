import sys
from typing import Union

# See https://mypy.readthedocs.io/en/stable/runtime_troubles.html#using-new-additions-to-the-typing-module
# See https://github.com/python/mypy/issues/8520
if sys.version_info >= (3, 8):
    from typing_extensions import Literal, TypedDict
else:
    from typing import Literal, TypedDict


class SinglePhoto(TypedDict):
    type: Literal["single_photo"]
    photo_id: str


class Album(TypedDict):
    type: Literal["album"]
    user_url: str
    album_id: str


class User(TypedDict):
    type: Literal["user"]
    user_url: str


class Group(TypedDict):
    type: Literal["group"]
    group_url: str


class Gallery(TypedDict):
    type: Literal["gallery"]
    gallery_id: str


class Tag(TypedDict):
    type: Literal["tag"]
    tag: str


ParseResult = Union[SinglePhoto, Album, User, Group, Gallery, Tag]
