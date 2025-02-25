import io
import wave

import numpy as np

from ggwave_python import GGWave, SampleFormat


def waveform_to_wav(
    waveform: bytes,
    sample_rate: int,
    sample_format: SampleFormat,
    channels: int,
) -> bytes:
    """Converts raw waveform bytes to a WAV file (as bytes), ensuring correct volume levels.

    Args:
        waveform (bytes): Raw audio data.
        sample_rate (int): Sample rate in Hz.
        sample_format (SampleFormat): Audio format (U8, I16, F32, etc.).
        channels (int): Number of audio channels.

    Returns:
        bytes: WAV file data.

    """
    sample_width = {SampleFormat.U8: 1, SampleFormat.I16: 2, SampleFormat.F32: 4}.get(
        sample_format,
        2,
    )

    if sample_format == SampleFormat.F32:
        waveform = np.frombuffer(waveform, dtype=np.float32)
        waveform = np.clip(waveform, -1.0, 1.0) * 32767
        waveform = waveform.astype(np.int16).tobytes()
        sample_width = 2

    elif sample_format == SampleFormat.U8:
        waveform = np.frombuffer(waveform, dtype=np.uint8)
        waveform = (waveform - 128).astype(np.int16).tobytes()
        sample_width = 2

    elif sample_format == SampleFormat.I8:
        waveform = np.frombuffer(waveform, dtype=np.int8)
        waveform = (waveform * 256).astype(np.int16).tobytes()
        sample_width = 2

    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as f:
        f.setnchannels(channels)
        f.setsampwidth(sample_width)
        f.setframerate(sample_rate)
        f.writeframes(waveform)

    return wav_buffer.getvalue()


def wav_to_waveform(
    wav_bytes: bytes,
    original_sample_format: SampleFormat,
) -> tuple[bytes, int, int]:
    """Converts a WAV file (as bytes) back to raw waveform data.

    Args:
        wav_bytes (bytes): WAV file data.
        original_sample_format (SampleFormat): The original format when encoded.

    Returns:
        tuple:
            - bytes: Raw audio data.
            - int: Sample rate.
            - int: Number of channels.

    """
    wav_buffer = io.BytesIO(wav_bytes)
    with wave.open(wav_buffer, 'rb') as f:
        sample_rate = f.getframerate()
        channels = f.getnchannels()
        waveform = f.readframes(f.getnframes())

    if original_sample_format == SampleFormat.F32:
        waveform = np.frombuffer(waveform, dtype=np.int16).astype(np.float32) / 32767
        waveform = waveform.tobytes()

    elif original_sample_format == SampleFormat.U8:
        waveform = np.frombuffer(waveform, dtype=np.int16).astype(np.uint8)
        waveform = (waveform + 128).tobytes()

    elif original_sample_format == SampleFormat.I8:
        waveform = np.frombuffer(waveform, dtype=np.int16).astype(np.int8)
        waveform = (waveform / 256).tobytes()

    return waveform, sample_rate, channels


def ggwave_to_waveform_params(ggwave_instance: GGWave) -> tuple[int, SampleFormat, int]:
    """Extracts sample rate, sample format, and channels from a GGWave instance.

    Args:
        ggwave_instance: An instance of GGWave.

    Returns:
        tuple:
            - int: Sample rate.
            - SampleFormat: Original GGWave format.
            - int: Number of channels.

    """
    sample_rate = ggwave_instance.parameters.get('sampleRateOut', 48000)
    sample_format = SampleFormat(ggwave_instance.parameters.get('sampleFormatOut', 5))
    return sample_rate, sample_format, 1  # Mono


def play_wav(wav_bytes: bytes):
    """Plays a WAV file from bytes using PyAudio.

    Args:
        wav_bytes (bytes): WAV file data.

    """
    import pyaudio

    # Read WAV parameters
    wav_buffer = io.BytesIO(wav_bytes)
    with wave.open(wav_buffer, 'rb') as f:
        sample_rate = f.getframerate()
        channels = f.getnchannels()
        sample_width = f.getsampwidth()
        waveform = f.readframes(f.getnframes())

    # Determine sample format
    sample_format = {
        1: pyaudio.paUInt8,
        2: pyaudio.paInt16,
        4: pyaudio.paFloat32,
    }.get(
        sample_width,
        pyaudio.paInt16,
    )  # Default to int16 if unknown

    # Convert to int16 for playback
    if sample_format == pyaudio.paFloat32:
        waveform = np.frombuffer(waveform, dtype=np.float32)
        waveform = np.clip(waveform, -1.0, 1.0) * 32767
        waveform = waveform.astype(np.int16).tobytes()

    elif sample_format == pyaudio.paUInt8:
        waveform = np.frombuffer(waveform, dtype=np.uint8)
        waveform = ((waveform - 128) * 256).astype(np.int16).tobytes()

    elif sample_format == pyaudio.paInt8:
        waveform = np.frombuffer(waveform, dtype=np.int8)
        waveform = (waveform * 256).astype(np.int16).tobytes()

    # Play the audio
    p = pyaudio.PyAudio()
    try:
        stream = p.open(
            format=pyaudio.paInt16,  # Always use int16 for playback
            channels=channels,
            rate=sample_rate,
            output=True,
        )

        chunk_size = 1024  # Optimal buffer size
        for i in range(0, len(waveform), chunk_size):
            stream.write(waveform[i : i + chunk_size])  # Play in chunks

        stream.stop_stream()
        stream.close()
    finally:
        p.terminate()
