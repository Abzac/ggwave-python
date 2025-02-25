import pytest

from ggwave_python import GGWave


@pytest.fixture(scope='session')
def ggwave():
    """Provides a GGWave instance for tests."""
    instance = GGWave()
    yield instance
    instance.free()


@pytest.fixture
def sample_message():
    return 'Hello, world!'
