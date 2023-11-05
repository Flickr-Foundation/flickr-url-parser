from typing import Generator

import pytest
from pytest import FixtureRequest
import vcr


@pytest.fixture(scope="function")
def cassette_name(request: FixtureRequest) -> str:
    # By default we use the name of the test as the cassette name,
    # but if it's a test parametrised with @pytest.mark.parametrize,
    # we include the parameter name to distinguish cassettes.
    #
    # See https://stackoverflow.com/a/67056955/1558022 for more info
    # on how this works.
    try:
        fixture_name = request.node.callspec.id.replace("/", "-").replace(":", "-")
        return f"{request.function.__name__}.{fixture_name}.yml"
    except AttributeError:
        return f"{request.function.__name__}.yml"


@pytest.fixture(scope="function")
def vcr_cassette(cassette_name: str) -> Generator[None, None, None]:
    """
    Creates a VCR cassette for use in tests.

    Anything using httpx in this test will record its HTTP interactions
    as "cassettes" using vcr.py, which can be replayed offline
    (e.g. in CI tests).
    """
    with vcr.use_cassette(
        cassette_name,
        cassette_library_dir="tests/fixtures/cassettes",
    ):
        yield
