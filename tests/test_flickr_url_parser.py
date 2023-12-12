from typing import Dict

import pytest

from flickr_url_parser import (
    parse_flickr_url,
    NotAFlickrUrl,
    UnrecognisedUrl,
)
from flickr_url_parser._types import Album, Gallery, Group, Tag


@pytest.mark.parametrize(
    "url",
    [
        "" "1.2.3.4",
        "https://example.net",
        "ftp://s3.amazonaws.com/my-bukkit/object.txt",
        "http://http://",
    ],
)
def test_it_rejects_a_url_which_isnt_flickr(url: str) -> None:
    with pytest.raises(NotAFlickrUrl):
        parse_flickr_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com",
        "https://www.flickr.com/account/email",
        # The characters in these examples are drawn from the
        # Unicode Numeric Property Definitions:
        # https://www.unicode.org/L2/L2012/12310-numeric-type-def.html
        #
        # In particular, all of these are characters that return True
        # for Python's ``str.isnumeric()`` function, but we don't expect
        # to see in a Flickr URL.
        "https://www.flickr.com/photos/fractions/½⅓¼⅕⅙⅐",
        "https://www.flickr.com/photos/circled/sets/①②③",
        "https://www.flickr.com/photos/numerics/galleries/Ⅰ፩൲〡",
        # A discussion page for a group
        "https://www.flickr.com/groups/slovenia/discuss/",
        # A malformed URL to a static photo
        "https://live.staticflickr.com/7372/help.jpg",
        "photos12.flickr.com/robots.txt",
    ],
)
def test_it_rejects_a_flickr_url_which_does_not_have_photos(url: str) -> None:
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/photos/coast_guard/32812033543",
        "http://www.flickr.com/photos/coast_guard/32812033543",
        "https://flickr.com/photos/coast_guard/32812033543",
        "http://flickr.com/photos/coast_guard/32812033543",
        "www.flickr.com/photos/coast_guard/32812033543",
        "flickr.com/photos/coast_guard/32812033543",
        "live.staticflickr.com/2903/32812033543_c1b3784192_w_d.jpg",
    ],
)
def test_it_can_parse_urls_even_if_the_host_is_a_bit_unusual(url: str) -> None:
    assert parse_flickr_url(url) == {
        "type": "single_photo",
        "photo_id": "32812033543",
    }


@pytest.mark.parametrize(
    ["url", "photo_id"],
    [
        ("https://www.flickr.com/photos/coast_guard/32812033543", "32812033543"),
        (
            "https://www.flickr.com/photos/coast_guard/32812033543/in/photolist-RZufqg-ebEcP7-YvCkaU-2dKrfhV-6o5anp-7ZjJuj-fxZTiu-2c1pGwi-JbqooJ-TaNkv5-ehrqn7-2aYFaRh-QLDxJX-2dKrdip-JB7iUz-ehrsNh-2aohZ14-Rgeuo3-JRwKwE-ksAR6U-dZVQ3m-291gkvk-26ynYWn-pHMQyE-a86UD8-9Tpmru-hamg6T-8ZCRFU-QY8amt-2eARQfP-qskFkD-2c1pG1Z-jbCpyF-fTBQDa-a89xfd-a7kYMs-dYjL51-5XJgXY-8caHdL-a89HZd-9GBmft-xy7PBo-sai77d-Vs8YPG-RgevC7-Nv5CF6-e4ZLn9-cPaxqS-9rnjS9-8Y7mhm",
            "32812033543",
        ),
        (
            "https://www.flickr.com/photos/britishlibrary/13874001214/in/album-72157644007437024/",
            "13874001214",
        ),
        ("https://www.Flickr.com/photos/techiedog/44257407", "44257407"),
        ("www.Flickr.com/photos/techiedog/44257407", "44257407"),
        (
            "https://www.flickr.com/photos/tanaka_juuyoh/1866762301/sizes/o/in/set-72157602201101937",
            "1866762301",
        ),
        ("https://www.flickr.com/photos/11588490@n02/2174280796/sizes/l", "2174280796"),
        ("https://www.flickr.com/photos/nrcs_south_dakota/8023844010/in", "8023844010"),
        (
            "https://www.flickr.com/photos/chucksutherland/6738252077/player/162ed63802",
            "6738252077",
        ),
        (
            "https://live.staticflickr.com/65535/53381630964_63d765ee92_s.jpg",
            "53381630964",
        ),
        ("photos12.flickr.com/16159487_3a6615a565_b.jpg", "16159487"),
    ],
)
def test_it_parses_a_single_photo(url: str, photo_id: str) -> None:
    assert parse_flickr_url(url) == {
        "type": "single_photo",
        "photo_id": photo_id,
    }


@pytest.mark.parametrize(
    ["url", "album"],
    [
        (
            "https://www.flickr.com/photos/cat_tac/albums/72157666833379009",
            {
                "type": "album",
                "user_url": "https://www.flickr.com/photos/cat_tac",
                "album_id": "72157666833379009",
                "page": 1,
            },
        ),
        (
            "https://www.flickr.com/photos/cat_tac/sets/72157666833379009",
            {
                "type": "album",
                "user_url": "https://www.flickr.com/photos/cat_tac",
                "album_id": "72157666833379009",
                "page": 1,
            },
        ),
        (
            "https://www.flickr.com/photos/andygocher/albums/72157648252420622/page3",
            {
                "type": "album",
                "user_url": "https://www.flickr.com/photos/andygocher",
                "album_id": "72157648252420622",
                "page": 3,
            },
        ),
    ],
)
def test_it_parses_an_album(url: str, album: Album) -> None:
    assert parse_flickr_url(url) == album


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("http://flic.kr/s/aHsjybZ5ZD", id="http-aHsjybZ5ZD"),
        pytest.param("https://flic.kr/s/aHsjybZ5ZD", id="https-aHsjybZ5ZD"),
    ],
)
def test_it_parses_a_short_album_url(vcr_cassette: str, url: str) -> None:
    assert parse_flickr_url(url) == {
        "type": "album",
        "user_url": "https://www.flickr.com/photos/64527945@N07",
        "album_id": "72157628959784871",
        "page": 1,
    }


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("http://flic.kr/s/---", id="dashes"),
        pytest.param("https://flic.kr/s/aaaaaaaaaaaaa", id="aaaaaaaaaaaaa"),
    ],
)
def test_it_doesnt_parse_bad_short_album_urls(vcr_cassette: str, url: str) -> None:
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/photos/blueminds/",
        "https://www.flickr.com/people/blueminds/",
        "https://www.flickr.com/photos/blueminds/albums",
    ],
)
def test_it_parses_a_user(url: str) -> None:
    assert parse_flickr_url(url) == {
        "type": "user",
        "user_url": "https://www.flickr.com/photos/blueminds",
        "page": 1,
    }


def test_it_gets_page_information_about_user_urls() -> None:
    assert parse_flickr_url("https://www.flickr.com/photos/blueminds/page3") == {
        "type": "user",
        "user_url": "https://www.flickr.com/photos/blueminds",
        "page": 3,
    }


def test_it_parses_a_short_user_url(vcr_cassette: str) -> None:
    assert parse_flickr_url("https://flic.kr/ps/ZVcni") == {
        "type": "user",
        "user_url": "https://www.flickr.com/photos/astrosamantha",
        "page": 1,
    }


@pytest.mark.parametrize(
    "url",
    [
        "https://flic.kr/ps",
        "https://flic.kr/ps/ZVcni/extra-bits",
        pytest.param("https://flic.kr/ps/ZZZZZZZZZ", id="ZZZZZZZZZ"),
    ],
)
def test_it_doesnt_parse_bad_short_user_urls(vcr_cassette: str, url: str) -> None:
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url)


@pytest.mark.parametrize(
    ["url", "group"],
    [
        (
            "https://www.flickr.com/groups/slovenia/pool/",
            {
                "type": "group",
                "group_url": "https://www.flickr.com/groups/slovenia",
                "page": 1,
            },
        ),
        (
            "https://www.flickr.com/groups/slovenia/",
            {
                "type": "group",
                "group_url": "https://www.flickr.com/groups/slovenia",
                "page": 1,
            },
        ),
        (
            "https://www.flickr.com/groups/slovenia/pool/page30",
            {
                "type": "group",
                "group_url": "https://www.flickr.com/groups/slovenia",
                "page": 30,
            },
        ),
    ],
)
def test_it_parses_a_group(url: str, group: Group) -> None:
    assert parse_flickr_url(url) == group


@pytest.mark.parametrize(
    ["url", "gallery"],
    [
        (
            "https://www.flickr.com/photos/flickr/gallery/72157722096057728/",
            {"type": "gallery", "gallery_id": "72157722096057728", "page": 1},
        ),
        (
            "https://www.flickr.com/photos/flickr/gallery/72157722096057728/page2",
            {"type": "gallery", "gallery_id": "72157722096057728", "page": 2},
        ),
        (
            "https://www.flickr.com/photos/flickr/galleries/72157722096057728/",
            {"type": "gallery", "gallery_id": "72157722096057728", "page": 1},
        ),
    ],
)
def test_it_parses_a_gallery(url: str, gallery: Gallery) -> None:
    assert parse_flickr_url(url) == gallery


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("https://flic.kr/y/2Xry4Jt", id="https-2Xry4Jt"),
        pytest.param("http://flic.kr/y/2Xry4Jt", id="http-2Xry4Jt"),
    ],
)
def test_it_parses_a_short_gallery(vcr_cassette: str, url: str) -> None:
    assert parse_flickr_url(url) == {
        "type": "gallery",
        "gallery_id": "72157690638331410",
        "page": 1,
    }


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("https://flic.kr/y/222222222222", id="222222222222"),
        "http://flic.kr/y/!!!",
    ],
)
def test_it_doesnt_parse_bad_short_gallery_urls(vcr_cassette: str, url: str) -> None:
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url)


@pytest.mark.parametrize(
    ["url", "tag"],
    [
        (
            "https://flickr.com/photos/tags/fluorspar/",
            {"type": "tag", "tag": "fluorspar", "page": 1},
        ),
        (
            "https://flickr.com/photos/tags/fluorspar/page1",
            {"type": "tag", "tag": "fluorspar", "page": 1},
        ),
        (
            "https://flickr.com/photos/tags/fluorspar/page5",
            {"type": "tag", "tag": "fluorspar", "page": 5},
        ),
    ],
)
def test_it_parses_a_tag(url: str, tag: Tag) -> None:
    assert parse_flickr_url(url) == tag


def test_it_parses_a_short_flickr_url() -> None:
    assert parse_flickr_url(url="https://flic.kr/p/2p4QbKN") == {
        "type": "single_photo",
        "photo_id": "53208249252",
    }


# Note: Guest Pass URLs are used to give somebody access to content
# on Flickr, even if (1) the content is private or (2) the person
# looking at the content isn't logged in.
#
# We should be a bit careful about test cases here, and only use
# Guest Pass URLs that have been shared publicly, to avoid accidentally
# sharing a public link to somebody's private photos.
#
# See https://www.flickrhelp.com/hc/en-us/articles/4404078163732-Change-your-privacy-settings
@pytest.mark.parametrize(
    ["url", "expected"],
    [
        # from https://twitter.com/PAPhotoMatt/status/1715111983974940683
        pytest.param(
            "https://www.flickr.com/gp/realphotomatt/M195SLkj98",
            {
                "type": "album",
                "user_url": "https://www.flickr.com/photos/realphotomatt",
                "album_id": "72177720312002426",
                "page": 1,
            },
            id="M195SLkj98",
        ),
        # one of mine (Alex's)
        pytest.param(
            "https://www.flickr.com/gp/199246608@N02/nSN80jZ64E",
            {"type": "single_photo", "photo_id": "53279364618"},
            id="nSN80jZ64E",
        ),
    ],
)
def test_it_parses_guest_pass_urls(
    vcr_cassette: str, url: str, expected: Dict[str, str]
) -> None:
    assert parse_flickr_url(url) == expected


def test_it_doesnt_parse_a_broken_guest_pass_url(vcr_cassette: str) -> None:
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url="https://www.flickr.com/gp/1234/doesnotexist")
