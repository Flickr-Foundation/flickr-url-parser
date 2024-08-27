"""
Re-export fixtures from silver-nitrate.
"""

from nitrate.cassettes import cassette_name, vcr_cassette

__all__ = ["cassette_name", "vcr_cassette"]
