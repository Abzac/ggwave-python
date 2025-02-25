import pytest

from ggwave_python import ProtocolId, optionals, waveform_utils


@pytest.mark.skipif(
    not optionals.PYAUDIO_ENABLED,
    reason='PyAudio is not installed, skipping audio tests',
)
def test_play_waveform(ggwave):
    """Test playing a waveform (should not raise an error)."""
    waveform = ggwave.encode('Test sound', ProtocolId.AUDIBLE_FAST, volume=20)
    try:
        waveform_utils.play_waveform(waveform)
    except Exception as e:
        pytest.fail(f'play_waveform raised an exception: {e}')


@pytest.mark.skipif(
    not optionals.PYAUDIO_ENABLED,
    reason='PyAudio is not installed, skipping audio tests',
)
def test_listen_generator():
    """Test that the listen method is a generator."""
    gen = waveform_utils.listen()

    assert hasattr(gen, '__iter__'), 'listen() should return a generator'
    assert hasattr(gen, '__next__'), 'listen() should return a generator'
