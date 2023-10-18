import json
import sys
import textwrap

from flickr_url_parser import parse_flickr_url


def run_cli(argv):
    try:
        url = argv[1]
    except IndexError:
        print(f"Usage: {__file__} <URL>", file=sys.stderr)
        return 1

    if url == "--help":
        print(textwrap.dedent(parse_flickr_url.__doc__).strip())
        return 0
    else:
        print(json.dumps(parse_flickr_url(url)))
        return 0


def main():  # pragma: no cover
    rc = run_cli(argv=sys.argv)
    sys.exit(rc)
