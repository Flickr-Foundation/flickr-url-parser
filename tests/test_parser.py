"""
Tests for ``flickr_url_parser.parser``.
"""

import pytest

from flickr_url_parser import looks_like_flickr_photo_id, looks_like_flickr_user_id


@pytest.mark.parametrize(
    "text",
    [
        # These are three real photo IDs
        "32812033543",
        "4895431370",
        "5240741057",
        # These aren't real photo IDs, but they look like they might be
        "1",
        "123",
        "12345678901234567890",
    ],
)
def test_looks_like_flickr_photo_id(text: str) -> None:
    """
    Any string made of digits 0-9 looks like a Flickr photo ID.
    """
    assert looks_like_flickr_photo_id(text)


@pytest.mark.parametrize("text", ["-1", "½", "cat.jpg", ""])
def test_doesnt_look_like_a_flickr_photo_id(text: str) -> None:
    """
    Any string not made of digits 0-9 doesn't look like a Flickr photo ID.
    """
    assert not looks_like_flickr_photo_id(text)


@pytest.mark.parametrize("text", ["47265398@N04"])
def test_looks_like_flickr_user_id(text: str) -> None:
    """
    Real Flickr user IDs look like Flickr user IDs.
    """
    assert looks_like_flickr_user_id(text)


@pytest.mark.parametrize("text", ["123", "blueminds", ""])
def test_doesnt_look_like_flickr_user_id(text: str) -> None:
    """
    These strings don't look like Flickr user IDs.
    """
    assert not looks_like_flickr_user_id(text)
