NUMPY_ENABLED = False
PYAUDIO_ENABLED = False

try:
    import numpy as np

    NUMPY_ENABLED = True
except ImportError:
    pass

try:
    import pyaudio

    PYAUDIO_ENABLED = True
except ImportError:
    pass


def _check_numpy():
    if not NUMPY_ENABLED:
        raise RuntimeError(
            "Numpy is not installed. Install it with 'pip install numpy'.",
        )
    return np


def _check_pyaudio():
    if not PYAUDIO_ENABLED:
        raise RuntimeError(
            "PyAudio is not installed. Install it with 'pip install pyaudio'.",
        )
    return pyaudio
