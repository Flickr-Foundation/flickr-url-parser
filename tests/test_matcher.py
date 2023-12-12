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
    ],
)
def test_find_flickr_urls_in_text(url: str) -> None:
    text = f"aaa {url} bbb"
    assert find_flickr_urls_in_text(text) == [url]
