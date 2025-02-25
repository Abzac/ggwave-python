import pytest

from ggwave_python import ProtocolId, wav_utils, waveform_utils


@pytest.fixture
def encoded_waveform(ggwave, sample_message):
    """Encodes a message into a waveform."""
    return ggwave.encode(sample_message, ProtocolId.AUDIBLE_FAST, volume=20)


def test_encode_decode_wav(ggwave, encoded_waveform, sample_message):
    """Test encoding into WAV, then decoding back."""
    sample_rate, sample_format, channels = wav_utils.ggwave_to_waveform_params(ggwave)

    # Convert waveform to WAV bytes
    wav_bytes = wav_utils.waveform_to_wav(encoded_waveform, sample_rate, sample_format, channels)

    # Convert WAV bytes back to waveform
    recovered_waveform, _, _ = wav_utils.wav_to_waveform(wav_bytes, sample_format)

    # Decode waveform
    decoded = ggwave.decode(recovered_waveform)

    assert decoded is not None, 'Decoded message should not be None'
    assert decoded.decode('utf-8') == sample_message, 'Decoded message should match original'


@pytest.mark.skipif(not waveform_utils.PYAUDIO_ENABLED, reason='PyAudio is not installed')
def test_play_wav(encoded_waveform, ggwave):
    """Test that play_wav does not raise errors."""
    sample_rate, sample_format, channels = wav_utils.ggwave_to_waveform_params(ggwave)
    wav_bytes = wav_utils.waveform_to_wav(encoded_waveform, sample_rate, sample_format, channels)

    try:
        wav_utils.play_wav(wav_bytes)
    except Exception as e:
        pytest.fail(f'play_wav raised an exception: {e}')
