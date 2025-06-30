"""
Tests for ``flickr_url_parser``.
"""

import pytest
from vcr.cassette import Cassette

from flickr_url_parser import (
    parse_flickr_url,
    NotAFlickrUrl,
    UnrecognisedUrl,
)
from flickr_url_parser.types import Album, Gallery, Group, SinglePhoto, Tag


@pytest.mark.parametrize(
    "url",
    [
        "",
        "1.2.3.4",
        "https://example.net",
        "ftp://s3.amazonaws.com/my-bukkit/object.txt",
        "http://http://",
        "#cite_note-1",
    ],
)
def test_it_rejects_a_url_which_isnt_flickr(url: str) -> None:
    """
    Any fragment of text which can be parsed as a URL but isn't
    a Flickr URL throws ``NotAFlickrUrl``.
    """
    with pytest.raises(NotAFlickrUrl):
        parse_flickr_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/account/email",
        "https://www.flickr.com/photo_zoom.gne",
        "https://www.flickr.com/photo_zoom.gne?id=unknown",
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
        "http://farm1.static.flickr.com/82/241abc183_dd0847d5c7_o.jpg",
        "https://farm5.staticflickr.com/4586/377abc695_bb4ecff5f4_o.jpg",
        "https://c8.staticflickr.com/6/5159/142abc431_7cf094b085_b.jpg",
        "farm3.static.flickr.com",
        "https://www.flickr.com/photo.gne?short=-1",
        "https://www.flickr.com/apps/video/stewart.swf?photo_id=-1",
        "https://commons.flickr.org/",
        "https://commons.flickr.org/about/",
    ],
)
def test_it_rejects_a_flickr_url_which_does_not_have_photos(url: str) -> None:
    """
    URLs on a Flickr.com domain which can't be identified throw
    ``UnrecognisedUrl``.
    """
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url)


@pytest.mark.parametrize("protocol", ["http://", "https://", ""])
@pytest.mark.parametrize("host", ["flickr.com", "www.flickr.com"])
def test_it_can_parse_variations_of_url(protocol: str, host: str) -> None:
    """
    A URL will be parsed consistently, even if there are variations in
    the protocol/domain.
    """
    url = f"{protocol}{host}/photos/coast_guard/32812033543"

    assert parse_flickr_url(url) == {
        "type": "single_photo",
        "photo_id": "32812033543",
        "user_url": "https://www.flickr.com/photos/coast_guard/",
        "user_id": None,
    }


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com",
        "https://www.flickr.com/",
        "http://www.flickr.com",
        "http://www.flickr.com/",
        "https://flickr.com",
        "https://flickr.com/",
        "http://flickr.com",
        "http://flickr.com/",
        "www.flickr.com",
        "flickr.com",
    ],
)
def test_it_can_parse_the_homepage(url: str) -> None:
    """
    It can parse different forms of the homepage URL, varying by:

    *   protocol
    *   domain name
    *   trailing slash or not

    """
    assert parse_flickr_url(url) == {"type": "homepage"}


@pytest.mark.parametrize(
    ["url", "single_photo"],
    [
        (
            "https://www.flickr.com/photos/coast_guard/32812033543",
            {
                "type": "single_photo",
                "photo_id": "32812033543",
                "user_url": "https://www.flickr.com/photos/coast_guard/",
                "user_id": None,
            },
        ),
        (
            "https://www.flickr.com/photos/coast_guard/32812033543/in/photolist-RZufqg-ebEcP7-YvCkaU-2dKrfhV-6o5anp-7ZjJuj-fxZTiu-2c1pGwi-JbqooJ-TaNkv5-ehrqn7-2aYFaRh-QLDxJX-2dKrdip-JB7iUz-ehrsNh-2aohZ14-Rgeuo3-JRwKwE-ksAR6U-dZVQ3m-291gkvk-26ynYWn-pHMQyE-a86UD8-9Tpmru-hamg6T-8ZCRFU-QY8amt-2eARQfP-qskFkD-2c1pG1Z-jbCpyF-fTBQDa-a89xfd-a7kYMs-dYjL51-5XJgXY-8caHdL-a89HZd-9GBmft-xy7PBo-sai77d-Vs8YPG-RgevC7-Nv5CF6-e4ZLn9-cPaxqS-9rnjS9-8Y7mhm",
            {
                "type": "single_photo",
                "photo_id": "32812033543",
                "user_url": "https://www.flickr.com/photos/coast_guard/",
                "user_id": None,
            },
        ),
        (
            "https://www.flickr.com/photos/britishlibrary/13874001214/in/album-72157644007437024/",
            {
                "type": "single_photo",
                "photo_id": "13874001214",
                "user_url": "https://www.flickr.com/photos/britishlibrary/",
                "user_id": None,
            },
        ),
        (
            "https://www.Flickr.com/photos/techiedog/44257407",
            {
                "type": "single_photo",
                "photo_id": "44257407",
                "user_url": "https://www.flickr.com/photos/techiedog/",
                "user_id": None,
            },
        ),
        (
            "www.Flickr.com/photos/techiedog/44257407",
            {
                "type": "single_photo",
                "photo_id": "44257407",
                "user_url": "https://www.flickr.com/photos/techiedog/",
                "user_id": None,
            },
        ),
        (
            "https://www.flickr.com/photos/tanaka_juuyoh/1866762301/sizes/o/in/set-72157602201101937",
            {
                "type": "single_photo",
                "photo_id": "1866762301",
                "user_url": "https://www.flickr.com/photos/tanaka_juuyoh/",
                "user_id": None,
            },
        ),
        #
        # Strictly speaking this URL is invalid, because of the lowercase @n02,
        # which should be uppercase.  But we know what you meant, so parse it anyway.
        (
            "https://www.flickr.com/photos/11588490@n02/2174280796/sizes/l",
            {
                "type": "single_photo",
                "photo_id": "2174280796",
                "user_url": "https://www.flickr.com/photos/11588490@N02/",
                "user_id": "11588490@N02",
            },
        ),
        (
            "https://www.flickr.com/photos/nrcs_south_dakota/8023844010/in",
            {
                "type": "single_photo",
                "photo_id": "8023844010",
                "user_url": "https://www.flickr.com/photos/nrcs_south_dakota/",
                "user_id": None,
            },
        ),
        (
            "https://www.flickr.com/photos/chucksutherland/6738252077/player/162ed63802",
            {
                "type": "single_photo",
                "photo_id": "6738252077",
                "user_url": "https://www.flickr.com/photos/chucksutherland/",
                "user_id": None,
            },
        ),
        (
            "http://flickr.com/photo/17277074@N00/2619974961",
            {
                "type": "single_photo",
                "photo_id": "2619974961",
                "user_url": "https://www.flickr.com/photos/17277074@N00/",
                "user_id": "17277074@N00",
            },
        ),
        (
            "http://flickr.com/photo/art-sarah/2619974961",
            {
                "type": "single_photo",
                "photo_id": "2619974961",
                "user_url": "https://www.flickr.com/photos/art-sarah/",
                "user_id": None,
            },
        ),
        (
            "https://www.flickr.com/photos/gracewong/196155401/meta/",
            {
                "type": "single_photo",
                "photo_id": "196155401",
                "user_url": "https://www.flickr.com/photos/gracewong/",
                "user_id": None,
            },
        ),
        #
        # From https://commons.wikimedia.org/wiki/File:75016-75017_Avenues_Foch_et_de_la_Grande_Armée_20050919.jpg
        # Retrieved 12 December 2023
        (
            "https://www.flickr.com/photos/joyoflife//44627174",
            {
                "type": "single_photo",
                "photo_id": "44627174",
                "user_url": "https://www.flickr.com/photos/joyoflife/",
                "user_id": None,
            },
        ),
    ],
)
def test_it_parses_a_single_photo_with_user_info(
    url: str, single_photo: SinglePhoto
) -> None:
    """
    It can parse different forms of single photo URL.
    """
    assert parse_flickr_url(url) == single_photo


@pytest.mark.parametrize(
    ["url", "photo_id"],
    [
        (
            "https://live.staticflickr.com/65535/53381630964_63d765ee92_s.jpg",
            "53381630964",
        ),
        ("photos12.flickr.com/16159487_3a6615a565_b.jpg", "16159487"),
        ("http://farm1.static.flickr.com/82/241708183_dd0847d5c7_o.jpg", "241708183"),
        ("farm1.static.flickr.com/82/241708183_dd0847d5c7_o.jpg", "241708183"),
        ("https://www.flickr.com/photo_zoom.gne?id=196155401&size=m", "196155401"),
        ("https://www.flickr.com/photo_exif.gne?id=1427904898", "1427904898"),
        # This URL is linked from https://commons.wikimedia.org/wiki/File:Adriaen_Brouwer_-_The_slaughter_feast.jpg
        (
            "https://farm5.staticflickr.com/4586/37767087695_bb4ecff5f4_o.jpg",
            "37767087695",
        ),
        #
        # From https://commons.wikimedia.org/wiki/File:Maradona_Soccer_Aid.jpg
        # Retrieved 12 December 2023
        ("static.flickr.com/63/155697786_0125559b4e.jpg", "155697786"),
        ("http://static.flickr.com/63/155697786_0125559b4e.jpg", "155697786"),
        #
        # From https://commons.wikimedia.org/wiki/File:Ice_Cream_Stand_on_Denman_Island.jpg
        # Retrieved 12 December 2023
        ("www.flickr.com/photo.gne?id=105", "105"),
        #
        # From https://commons.wikimedia.org/wiki/File:IgnazioDanti.jpg
        # Retrieved 12 December 2023
        ("c8.staticflickr.com/6/5159/14288803431_7cf094b085_b.jpg", "14288803431"),
        #
        # From https://commons.wikimedia.org/wiki/File:The_Peace_Hat_and_President_Chester_Arthur,_1829_-_1886_(3435827496).jpg
        # Retrieved 20 December 2023
        ("www.flickr.com/photo_edit.gne?id=3435827496", "3435827496"),
        #
        # From https://commons.wikimedia.org/wiki/File:Mars_-_Valles_Marineris,_Melas_Chasma_-_ESA_Mars_Express_(52830681359).png
        # Retrieved 20 December 2023
        ("https://www.flickr.com/photo.gne?short=2ouuqFT", "52830949513"),
        #
        # This is the download URL from https://www.flickr.com/photos/196406308@N04/52947513801
        # Retrieved 2 January 2024
        ("https://www.flickr.com/video_download.gne?id=52947513801", "52947513801"),
        #
        # This is the download URL you get redirected to from
        # https://www.flickr.com/photos/83699771@N00/52868534222
        # Retrieved 2 January 2024
        (
            "https://live.staticflickr.com/video/52868534222/346a41e5a9/1080p.mp4",
            "52868534222",
        ),
        #
        # This URL comes from the flickr.photos.getSizes API for
        # this photo.
        # Retrieved 2 January 2024
        (
            "https://www.flickr.com/apps/video/stewart.swf?v=2968162862&photo_id=53262935176&photo_secret=06c382eee3",
            "53262935176",
        ),
    ],
)
def test_it_parses_a_single_photo_without_user_info(url: str, photo_id: str) -> None:
    """
    Parse variants of the single photo URL that don't give any information
    about the photo's owner.
    """
    assert parse_flickr_url(url) == {
        "type": "single_photo",
        "photo_id": photo_id,
        "user_url": None,
        "user_id": None,
    }


def test_it_parses_a_short_flickr_url() -> None:
    """
    Parse a short URL which redirects to a single photo.
    """
    assert parse_flickr_url(url="https://flic.kr/p/2p4QbKN") == {
        "type": "single_photo",
        "photo_id": "53208249252",
        "user_url": None,
        "user_id": None,
    }


@pytest.mark.parametrize(
    ["url", "album"],
    [
        (
            "https://www.flickr.com/photos/cat_tac/albums/72157666833379009",
            {
                "type": "album",
                "user_url": "https://www.flickr.com/photos/cat_tac/",
                "album_id": "72157666833379009",
                "page": 1,
            },
        ),
        (
            "https://www.flickr.com/photos/cat_tac/sets/72157666833379009",
            {
                "type": "album",
                "user_url": "https://www.flickr.com/photos/cat_tac/",
                "album_id": "72157666833379009",
                "page": 1,
            },
        ),
        (
            "https://www.flickr.com/photos/andygocher/albums/72157648252420622/page3",
            {
                "type": "album",
                "user_url": "https://www.flickr.com/photos/andygocher/",
                "album_id": "72157648252420622",
                "page": 3,
            },
        ),
    ],
)
def test_it_parses_an_album(url: str, album: Album) -> None:
    """
    Parse album URLs.
    """
    assert parse_flickr_url(url) == album


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("http://flic.kr/s/aHsjybZ5ZD", id="http-aHsjybZ5ZD"),
        pytest.param("https://flic.kr/s/aHsjybZ5ZD", id="https-aHsjybZ5ZD"),
    ],
)
def test_it_parses_a_short_album_url(vcr_cassette: Cassette, url: str) -> None:
    """
    Parse short URLs which redirect to albums.
    """
    assert parse_flickr_url(url, follow_redirects=True) == {
        "type": "album",
        "user_url": "https://www.flickr.com/photos/64527945@N07/",
        "album_id": "72157628959784871",
        "page": 1,
    }


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("http://flic.kr/s/", id="http-s"),
        pytest.param("http://flic.kr/s/---", id="dashes"),
        pytest.param("https://flic.kr/s/aaaaaaaaaaaaa", id="aaaaaaaaaaaaa"),
    ],
)
def test_it_doesnt_parse_bad_short_album_urls(vcr_cassette: Cassette, url: str) -> None:
    """
    Parsing a short URL which looks like an album but doesn't redirect
    to one throws ``UnrecognisedUrl``
    """
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/photos/blueminds/",
        "https://www.flickr.com/people/blueminds/",
        "https://www.flickr.com/photos/blueminds/albums",
        "https://www.flickr.com/photos/blueminds/?saved=1",
    ],
)
def test_it_parses_a_user(url: str) -> None:
    """
    Parse a user's profile URL with a path alias.
    """
    assert parse_flickr_url(url) == {
        "type": "user",
        "user_url": "https://www.flickr.com/photos/blueminds/",
        "user_id": None,
        "page": 1,
    }


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/photos/47265398@N04/",
        "https://www.flickr.com/people/47265398@N04/",
        "https://www.flickr.com/photos/47265398@N04/albums",
        "https://www.flickr.com/photos/47265398@N04/?saved=1",
    ],
)
def test_it_parses_a_user_with_id(url: str) -> None:
    """
    Parse a user's profile URL with their NSID.
    """
    assert parse_flickr_url(url) == {
        "type": "user",
        "user_url": "https://www.flickr.com/photos/47265398@N04/",
        "user_id": "47265398@N04",
        "page": 1,
    }


def test_parses_a_commons_explorer_url_with_path_alias() -> None:
    """
    Parse a Commons Explorer member page URL with a path alias.
    """
    url = "https://commons.flickr.org/members/swedish_heritage_board/"

    assert parse_flickr_url(url) == {
        "type": "user",
        "user_url": "https://www.flickr.com/photos/swedish_heritage_board/",
        "user_id": None,
        "page": 1,
    }


def test_parses_a_commons_explorer_url_with_user_id() -> None:
    """
    Parse a Commons Explorer member page URL with a user ID.
    """
    url = "https://commons.flickr.org/members/107895189@N03/"

    assert parse_flickr_url(url) == {
        "type": "user",
        "user_url": "https://www.flickr.com/photos/107895189@N03/",
        "user_id": "107895189@N03",
        "page": 1,
    }


def test_it_gets_page_information_about_user_urls() -> None:
    """
    Get the page number from a paginated URL in a user's photostream.
    """
    assert parse_flickr_url("https://www.flickr.com/photos/blueminds/page3") == {
        "type": "user",
        "user_url": "https://www.flickr.com/photos/blueminds/",
        "user_id": None,
        "page": 3,
    }


def test_it_parses_a_short_user_url(vcr_cassette: Cassette) -> None:
    """
    Parse a short URL which redirects to a user's photostream.
    """
    assert parse_flickr_url("https://flic.kr/ps/ZVcni", follow_redirects=True) == {
        "type": "user",
        "user_url": "https://www.flickr.com/photos/astrosamantha/",
        "user_id": None,
        "page": 1,
    }


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("https://flic.kr/ps", id="ps"),
        pytest.param("https://flic.kr/ps/ZVcni/extra-bits", id="extra-bits"),
        pytest.param("https://flic.kr/ps/ZZZZZZZZZ", id="ZZZZZZZZZ"),
    ],
)
@pytest.mark.parametrize("follow_redirects", [True, False])
def test_it_doesnt_parse_bad_short_user_urls(
    vcr_cassette: Cassette, url: str, follow_redirects: bool
) -> None:
    """
    Parsing a short URL which has the `/ps` path component for a photostream
    but doesn't redirect to one throws ``UnrecognisedUrl``
    """
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url, follow_redirects=follow_redirects)


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
    """
    Parse URLs to a group.
    """
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
    """
    Parse gallery URLs.
    """
    assert parse_flickr_url(url) == gallery


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("https://flic.kr/y/2Xry4Jt", id="https-2Xry4Jt"),
        pytest.param("http://flic.kr/y/2Xry4Jt", id="http-2Xry4Jt"),
    ],
)
def test_it_parses_a_short_gallery(vcr_cassette: Cassette, url: str) -> None:
    """
    Parse a short URL which redirects to a gallery.
    """
    assert parse_flickr_url(url, follow_redirects=True) == {
        "type": "gallery",
        "gallery_id": "72157690638331410",
        "page": 1,
    }


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("https://flic.kr/y/222222222222", id="222222222222"),
        pytest.param("http://flic.kr/y/!!!", id="!!!"),
    ],
)
def test_it_doesnt_parse_bad_short_gallery_urls(
    vcr_cassette: Cassette, url: str
) -> None:
    """
    Parsing a short URL which has the `/y` path component for a gallery
    but doesn't redirect to one throws ``UnrecognisedUrl``.
    """
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
    """
    Parse tag URLs.
    """
    assert parse_flickr_url(url) == tag


GUEST_PASS_URL_TEST_CASES = [
    # from https://twitter.com/PAPhotoMatt/status/1715111983974940683
    pytest.param(
        "https://www.flickr.com/gp/realphotomatt/M195SLkj98",
        {
            "type": "album",
            "user_url": "https://www.flickr.com/photos/realphotomatt/",
            "album_id": "72177720312002426",
            "page": 1,
        },
        id="M195SLkj98",
    ),
    # one of mine (Alex's)
    pytest.param(
        "https://www.flickr.com/gp/199246608@N02/nSN80jZ64E",
        {
            "type": "single_photo",
            "photo_id": "53279364618",
            "user_url": "https://www.flickr.com/photos/199246608@N02/",
            "user_id": "199246608@N02",
        },
        id="nSN80jZ64E",
    ),
]


@pytest.mark.parametrize(["url", "expected"], GUEST_PASS_URL_TEST_CASES)
def test_it_parses_guest_pass_urls(
    vcr_cassette: Cassette, url: str, expected: dict[str, str]
) -> None:
    """
    Parse guest pass URLs.

    Note: Guest Pass URLs are used to give somebody access to content
    on Flickr, even if (1) the content is private or (2) the person
    looking at the content isn't logged in.

    We should be a bit careful about test cases here, and only use
    Guest Pass URLs that have been shared publicly, to avoid accidentally
    sharing a public link to somebody's private photos.

    See https://www.flickrhelp.com/hc/en-us/articles/4404078163732-Change-your-privacy-settings
    """
    assert parse_flickr_url(url, follow_redirects=True) == expected


@pytest.mark.parametrize(["url", "expected"], GUEST_PASS_URL_TEST_CASES)
def test_no_guest_pass_if_no_follow_redirects(
    url: str, expected: dict[str, str]
) -> None:
    """
    Guest pass URLs aren't parsed if `follow_redirects=False`.
    """
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url, follow_redirects=False)


def test_it_doesnt_parse_a_broken_guest_pass_url(vcr_cassette: Cassette) -> None:
    """
    Parsing a URL which has the `/gp` path component for a guest pass
    but doesn't redirect to one throws ``UnrecognisedUrl``.
    """
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(
            url="https://www.flickr.com/gp/1234/doesnotexist", follow_redirects=True
        )


def test_a_non_string_is_an_error() -> None:
    """
    Parsing a non-string/non-URL value throws ``UnrecognisedUrl``.
    """
    with pytest.raises(TypeError, match="Bad type for `url`: expected str, got int!"):
        parse_flickr_url(url=-1)  # type: ignore
