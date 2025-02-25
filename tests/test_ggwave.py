from ggwave_python import ProtocolId


def test_encode_decode(ggwave, sample_message):
    """Test encoding and decoding of a simple message."""
    waveform = ggwave.encode(sample_message, ProtocolId.AUDIBLE_FAST, volume=20)
    decoded = ggwave.decode(waveform)

    assert decoded is not None, 'Decoded message should not be None'
    assert decoded.decode('utf-8') == sample_message, 'Decoded message should match original'


def test_empty_message(ggwave):
    """Test encoding and decoding of an empty message."""
    waveform = ggwave.encode('', ProtocolId.AUDIBLE_FAST, volume=20)
    decoded = ggwave.decode(waveform)

    assert decoded == b'', 'Decoded message should be empty'


def test_invalid_waveform(ggwave):
    """Test decoding an invalid waveform (should return None)."""
    invalid_waveform = b'\x00\x01\x02\x03\x04'
    decoded = ggwave.decode(invalid_waveform)

    assert decoded == b'', 'Decoding invalid waveform should return None'
