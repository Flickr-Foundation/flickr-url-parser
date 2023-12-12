import pytest

from flickr_url_parser import find_flickr_urls_in_text


@pytest.mark.parametrize(
    "url",
    [
        "https://www.flickr.com",
        "https://www.flickr.com/account/email",
        "https://www.flickr.com/groups/slovenia/discuss/",
        "https://live.staticflickr.com/7372/help.jpg",
        "http://flickr.com/photos/coast_guard/32812033543",
        "http://farm3.static.flickr.com/2060/2264610973_3989a4627f_o.jpg",
        "https://www.flickr.com/photo_zoom.gne?id=196155401&size=m",
        "http://photos4.flickr.com/4891733_cec6cd1c66_b_d.jpg",
        "https://farm5.static.flickr.com/4586/37767087695_bb4ecff5f4_o.jpg",
        #
        # From https://commons.wikimedia.org/wiki/File:Adriaen_Brouwer_-_The_slaughter_feast.jpg
        # Retrieved 12 December 2023
        "https://farm5.staticflickr.com/4586/37767087695_bb4ecff5f4_o.jpg",
        #
        # From https://commons.wikimedia.org/wiki/File:Maradona_Soccer_Aid.jpg
        # Retrieved 12 December 2023
        "http://static.flickr.com/63/155697786_0125559b4e.jpg",
    ],
)
def test_find_flickr_urls_in_text(url: str) -> None:
    text = f"aaa {url} bbb"
    assert find_flickr_urls_in_text(text) == [url]
