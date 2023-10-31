from typing import TypedDict, Union

try:
    from typing import Literal
except ImportError as e:  # Python 3.7
    from typing_extensions import Literal


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
