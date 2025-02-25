from collections.abc import Generator

from ggwave_python.optionals import _check_pyaudio

GGWAVE_UNSET = object()


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
    pyaudio = _check_pyaudio()

    if sample_format is GGWAVE_UNSET:
        sample_format = pyaudio.paFloat32  # Default to 32-bit float

    p = pyaudio.PyAudio()

    try:
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
    finally:
        p.terminate()


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
    pyaudio = _check_pyaudio()

    p = pyaudio.PyAudio()

    try:
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
        finally:
            stream.stop_stream()
            stream.close()

    except KeyboardInterrupt:
        pass
    finally:
        p.terminate()
