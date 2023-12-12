import re


FLICKR_URL_RE_MATCH = re.compile(
    r"(?:https?://)"
    r"?(?:www\.)?"
    r"(?:live\.static\.?)?"
    r"(?:farm[0-9]+\.static\.?)?"
    r"(?:photos[0-9]+\.)?"
    r"flickr\.com[0-9A-Za-z@_\-/\.\?\&=]*"
)


def find_flickr_urls_in_text(text: str) -> list[str]:
    """
    Returns a list of Flickr URLs in a block of text (if any).
    """
    return FLICKR_URL_RE_MATCH.findall(text)
