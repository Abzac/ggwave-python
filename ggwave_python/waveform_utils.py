from collections.abc import Generator

PYAUDIO_ENABLED = False

try:
    import pyaudio

    PYAUDIO_ENABLED = True
except ImportError:
    pass


GGWAVE_UNSET = object()


def _check_pyaudio():
    if not PYAUDIO_ENABLED:
        raise RuntimeError(
            "PyAudio is not installed. Install it with 'pip install pyaudio'.",
        )
    return pyaudio.PyAudio()


def play_waveform(
    waveform: bytes,
    sample_rate: int = 48000,
    channels: int = 1,
    sample_format: int | None = GGWAVE_UNSET,
):
    """Plays an audio waveform using the system's default output device.

    Args:
        waveform: The audio data to be played.
        sample_rate: The sample rate of the waveform (default: 48000 Hz).
        channels: The number of audio channels (default: 1).
        sample_format: The audio sample format (default: float32).

    """
    p = _check_pyaudio()

    if sample_format is GGWAVE_UNSET:
        sample_format = pyaudio.paFloat32  # Default to 32-bit float

    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=sample_rate,
        output=True,
    )

    try:
        stream.write(waveform)
    finally:
        stream.stop_stream()
        stream.close()


def listen(
    sample_rate: int = 48000,
    chunk_size: int = 1024,
    channels: int = 1,
) -> Generator[bytes, None, None]:
    """Continuously listens for incoming audio.

    Args:
        sample_rate: The input sample rate in Hz (default: 48000).
        chunk_size: The number of samples per frame (default: 1024).
        channels: The number of audio input channels (default: 1).

    Yields:
        Audio data as byte sequences.

    """
    p = _check_pyaudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    try:
        while True:
            yield stream.read(chunk_size, exception_on_overflow=False)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
