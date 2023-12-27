from typing import Literal, NotRequired, TypedDict


class Homepage(TypedDict):
    type: Literal["homepage"]


class SinglePhoto(TypedDict):
    type: Literal["single_photo"]
    photo_id: str


class Album(TypedDict):
    type: Literal["album"]
    user_url: str
    album_id: str
    page: int


class User(TypedDict):
    type: Literal["user"]
    page: int
    user_url: str
    id: NotRequired[str]


class Group(TypedDict):
    type: Literal["group"]
    group_url: str
    page: int


class Gallery(TypedDict):
    type: Literal["gallery"]
    gallery_id: str
    page: int


class Tag(TypedDict):
    type: Literal["tag"]
    tag: str
    page: int


ParseResult = Homepage | SinglePhoto | Album | User | Group | Gallery | Tag
