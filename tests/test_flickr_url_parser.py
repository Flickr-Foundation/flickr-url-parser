import pytest

from flickr_url_parser import parse_flickr_url, NotAFlickrUrl, UnrecognisedUrl


@pytest.mark.parametrize(
    "url",
    [
        "" "1.2.3.4",
        "https://example.net",
        "ftp://s3.amazonaws.com/my-bukkit/object.txt",
        "http://http://",
    ],
)
def test_it_rejects_a_url_which_isnt_flickr(url):
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
    ],
)
def test_it_rejects_a_flickr_url_which_does_have_photos(url):
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
    ],
)
def test_it_can_parse_urls_even_if_the_host_is_a_bit_unusual(url):
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
    ],
)
def test_it_parses_a_single_photo(url, photo_id):
    assert parse_flickr_url(url) == {
        "type": "single_photo",
        "photo_id": photo_id,
    }


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/photos/cat_tac/albums/72157666833379009",
        "https://www.flickr.com/photos/cat_tac/sets/72157666833379009",
    ],
)
def test_it_parses_an_album(url):
    assert parse_flickr_url(url) == {
        "type": "album",
        "user_url": "https://www.flickr.com/photos/cat_tac",
        "album_id": "72157666833379009",
    }


@pytest.mark.parametrize(
    "url",
    [
        "http://flic.kr/s/aHsjybZ5ZD",
        "https://flic.kr/s/aHsjybZ5ZD",
    ],
)
def test_it_parses_a_short_album_url(vcr_cassette, url):
    assert parse_flickr_url(url) == {
        "type": "album",
        "user_url": "https://www.flickr.com/photos/64527945@N07",
        "album_id": "72157628959784871",
    }


@pytest.mark.parametrize(
    "url",
    [
        "http://flic.kr/s/---",
        "https://flic.kr/s/aaaaaaaaaaaaa",
    ],
)
def test_it_doesnt_parse_bad_short_album_urls(vcr_cassette, url):
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/photos/blueminds/",
        "https://www.flickr.com/people/blueminds/",
        "https://www.flickr.com/photos/blueminds/albums",
        "https://www.flickr.com/photos/blueminds/page3",
    ],
)
def test_it_parses_a_user(url):
    assert parse_flickr_url(url) == {
        "type": "user",
        "user_url": "https://www.flickr.com/photos/blueminds",
    }


def test_it_parses_a_short_user_url(vcr_cassette):
    assert parse_flickr_url("https://flic.kr/ps/ZVcni") == {
        "type": "user",
        "user_url": "https://www.flickr.com/photos/astrosamantha",
    }


@pytest.mark.parametrize(
    "url",
    [
        "https://flic.kr/ps",
        "https://flic.kr/ps/ZVcni/extra-bits",
        "https://flic.kr/ps/ZZZZZZZZZ",
    ],
)
def test_it_doesnt_parse_bad_short_user_urls(vcr_cassette, url):
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/groups/slovenia/pool/",
        "https://www.flickr.com/groups/slovenia/",
        "https://www.flickr.com/groups/slovenia/pool/page30",
    ],
)
def test_it_parses_a_group(url):
    assert parse_flickr_url(url) == {
        "type": "group",
        "group_url": "https://www.flickr.com/groups/slovenia",
    }


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com/photos/flickr/gallery/72157722096057728/",
        "https://www.flickr.com/photos/flickr/gallery/72157722096057728/page2",
        "https://www.flickr.com/photos/flickr/galleries/72157722096057728/",
    ],
)
def test_it_parses_a_gallery(url):
    assert parse_flickr_url(url) == {
        "type": "gallery",
        "gallery_id": "72157722096057728",
    }


@pytest.mark.parametrize(
    "url", ["https://flic.kr/y/2Xry4Jt", "http://flic.kr/y/2Xry4Jt"]
)
def test_it_parses_a_short_gallery(vcr_cassette, url):
    assert parse_flickr_url(url) == {
        "type": "gallery",
        "gallery_id": "72157690638331410",
    }


@pytest.mark.parametrize(
    "url", ["https://flic.kr/y/222222222222", "http://flic.kr/y/!!!"]
)
def test_it_doesnt_parse_bad_short_gallery_urls(vcr_cassette, url):
    with pytest.raises(UnrecognisedUrl):
        parse_flickr_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://flickr.com/photos/tags/fluorspar/",
        "https://flickr.com/photos/tags/fluorspar/page1",
    ],
)
def test_it_parses_a_tag(url):
    assert parse_flickr_url(url) == {
        "type": "tag",
        "tag": "fluorspar",
    }


def test_it_parses_a_short_flickr_url():
    assert parse_flickr_url(url="https://flic.kr/p/2p4QbKN") == {
        "type": "single_photo",
        "photo_id": "53208249252",
    }
