import json

from flickr_url_parser.cli import run_cli


def test_run_cli(capsys):
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
    }
    assert captured.err == ""


def test_run_cli_shows_help(capsys):
    rc = run_cli(argv=["flickr_url_parser", "--help"])

    assert rc == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("Parse a Flickr URL and return some key information")
    assert captured.err == ""


def test_run_cli_throws_err(capsys):
    rc = run_cli(argv=["flickr_url_parser"])

    assert rc == 1

    captured = capsys.readouterr()
    assert captured.out.startswith("")
    assert captured.err.startswith("Usage:")
