"""
Tests for the flickr_url_parser CLI.
"""

import json

from pytest import CaptureFixture

from flickr_url_parser.cli import run_cli


def test_run_cli(capsys: CaptureFixture[str]) -> None:
    """
    Running ``flickr_url_parser URL`` prints the parsed URL as JSON.
    """
    rc = run_cli(
        argv=[
            "flickr_url_parser",
            "https://www.flickr.com/photos/coast_guard/32812033543",
        ]
    )

    assert rc == 0

    captured = capsys.readouterr()
    assert json.loads(captured.out) == {
        "type": "single_photo",
        "photo_id": "32812033543",
        "user_url": "https://www.flickr.com/photos/coast_guard/",
        "user_id": None,
    }
    assert captured.err == ""


def test_run_cli_shows_help(capsys: CaptureFixture[str]) -> None:
    """
    Running ``flickr_url_parser --help`` prints the help message.
    """
    rc = run_cli(argv=["flickr_url_parser", "--help"])

    assert rc == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("Parse a Flickr URL and return some key information")
    assert captured.err == ""


def test_run_cli_shows_version(capsys: CaptureFixture[str]) -> None:
    """
    Running ``flickr_url_parser --version`` prints the version number.
    """
    rc = run_cli(argv=["flickr_url_parser", "--version"])

    assert rc == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("flickr_url_parser 1.")
    assert captured.err == ""


def test_run_cli_throws_err(capsys: CaptureFixture[str]) -> None:
    """
    Running ``flickr_url_parser`` without a URL is an error.
    """
    rc = run_cli(argv=["flickr_url_parser"])

    assert rc == 1

    captured = capsys.readouterr()
    assert captured.out.startswith("")
    assert captured.err.startswith("Usage:")
