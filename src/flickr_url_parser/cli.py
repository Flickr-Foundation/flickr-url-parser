import json
import sys
import textwrap

from . import parse_flickr_url, __version__


def run_cli(argv: list[str]) -> int:
    try:
        url = argv[1]
    except IndexError:
        print(f"Usage: {__file__} <URL>", file=sys.stderr)
        return 1

    if url == "--help":
        print(textwrap.dedent(parse_flickr_url.__doc__).strip())  # type: ignore[arg-type]
        return 0
    elif url == "--version":
        print(f"flickr_url_parser {__version__}")
        return 0
    else:
        print(json.dumps(parse_flickr_url(url)))
        return 0


def main() -> None:  # pragma: no cover
    rc = run_cli(argv=sys.argv)
    sys.exit(rc)
