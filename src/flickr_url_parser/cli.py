"""
Basic CLI for ``flickr_url_parser``.
"""

import json
import sys
import textwrap

from . import parse_flickr_url, __version__


def run_cli(argv: list[str]) -> int:
    """
    Parse the command-line arguments and return an exit code.

    Possible uses:

    1.  Pass a URL as a command-line argument, e.g.

            flickr_url_parser https://flickr.com

    2.  Pass the ``-help`` flag to get help text:

            flickr_url_parser --help

    3.  Pass the ``--version`` flag to get the version number:

            flickr_url_parser --version

    """
    # Because this interface is so simple, I just implemented it
    # manually.  If we want to make it any more complicated, we should
    # use a proper library for parsing command-line arguments,
    # e.g. ``argparse`` or ``click``
    try:
        single_arg = argv[1]
    except IndexError:
        print(f"Usage: {__file__} <URL>", file=sys.stderr)
        return 1

    if single_arg == "--help":
        print(textwrap.dedent(parse_flickr_url.__doc__).strip())  # type: ignore[arg-type]
        return 0
    elif single_arg == "--version":
        print(f"flickr_url_parser {__version__}")
        return 0
    else:
        print(json.dumps(parse_flickr_url(single_arg)))
        return 0


def main() -> None:  # pragma: no cover
    """
    Actually run the CLI and exit the program with the returned exit code.
    """
    rc = run_cli(argv=sys.argv)
    sys.exit(rc)
