from enum import IntEnum, IntFlag

import ggwave

GGWAVE_UNSET = object()  # Sentinel value to distinguish unset parameters


class SampleFormat(IntEnum):
    """Represents the audio sample format used in GGWave."""

    UNDEFINED = 0
    U8 = 1  # Unsigned 8-bit
    I8 = 2  # Signed 8-bit
    U16 = 3  # Unsigned 16-bit
    I16 = 4  # Signed 16-bit
    F32 = 5  # 32-bit floating point


class ProtocolId(IntEnum):
    """Defines different transmission protocols available in GGWave.

    # Modulation (Tx)

    The current approach uses a multi-frequency Frequency-Shift Keying (FSK) modulation scheme.
    The data to be transmitted is first split into 4-bit chunks.
    At each moment of time, 3 bytes are transmitted using 6 tones - one tone for each 4-bit chunk.
    The 6 tones are emitted in a 4.5kHz range divided in 96 equally-spaced frequencies

    Freq_Hz = F0 + chunk_no * dF

    For all protocols: dF = 46.875 Hz.
    For non-ultrasonic protocols: F0 = 1875.000 Hz.
    For ultrasonic protocols: F0 = 15000.000 Hz.

    The original data is encoded using Reed-Solomon error codes.
    The number of ECC bytes is determined based on the length of the original data.
    The encoded data is the one being transmitted.

    # Demodulation (Rx)

    Beginning and ending of the transmission are marked with special sound markers.
    The receiver listens for these markers and records the in-between sound data.
    The recorded data is then Fourier transformed to obtain a frequency spectrum.
    The detected frequencies are decoded back to binary data in the same way they were encoded.

    Reed-Solomon decoding is finally performed to obtain the original data.

    # Markers

    The begin marker uses the first 32 frequency bins: F0 + 00*df to F0 + 31*df.
    We produce a waveform which consists of 16 frequencies:

    F0 + 00*df
    F0 + 03*df
    F0 + 04*df
    F0 + 07*df
    F0 + 08*df
    F0 + 11*df
    F0 + 12*df
    F0 + 15*df
    F0 + 16*df
    F0 + 19*df
    F0 + 20*df
    F0 + 23*df
    F0 + 24*df
    F0 + 27*df
    F0 + 28*df
    F0 + 31*df

    The end marker consists again of 16 frequencies - the ones that are missing in the begin marker.
    For each frame of input samples, compute the FFT and analyze the 32 bins.
    """

    AUDIBLE_NORMAL = 0  # Standard audible range transmission
    AUDIBLE_FAST = 1
    AUDIBLE_FASTEST = 2
    ULTRASOUND_NORMAL = 3  # Ultrasound transmission (above human hearing)
    ULTRASOUND_FAST = 4
    ULTRASOUND_FASTEST = 5
    DT_NORMAL = 6  # Dual-tone protocol (DTMF-like)
    DT_FAST = 7
    DT_FASTEST = 8
    MT_NORMAL = 9  # Multi-tone protocol (higher data rates)
    MT_FAST = 10
    MT_FASTEST = 11
    CUSTOM_0 = 12  # Custom user-defined protocol
    CUSTOM_1 = 13
    CUSTOM_2 = 14
    CUSTOM_3 = 15
    CUSTOM_4 = 16
    CUSTOM_5 = 17
    CUSTOM_6 = 18
    CUSTOM_7 = 19
    CUSTOM_8 = 20
    CUSTOM_9 = 21


class Filter(IntEnum):
    """Available filter types for signal processing in GGWave."""

    HANN = 0  # Hann window function
    HAMMING = 1  # Hamming window function
    FIRST_ORDER_HIGH_PASS = 2  # First-order high-pass filter


class OperatingMode(IntFlag):
    """Defines the operating modes for a GGWave instance."""

    RX = 1 << 1  # Enable receiving audio data
    TX = 1 << 2  # Enable transmitting audio data
    RX_AND_TX = RX | TX  # Enable both Rx and Tx
    TX_ONLY_TONES = 1 << 3  # Encode as tone sequence instead of full waveform
    USE_DSS = 1 << 4  # Enable Direct Sequence Spread (DSS) algorithm


class GGWave:
    """A high-level Python wrapper for the GGWave audio communication library."""

    MAX_INSTANCES = 4  # Hardcoded limit in GGWave
    _instances_count = 0  # Active instances counter

    def __init__(  # noqa: PLR0913 Too many arguments in function definition
        self,
        payload_length: int | None = GGWAVE_UNSET,  # Default: -1 (variable length)
        sample_rate_inp: float | None = GGWAVE_UNSET,  # Default: 48000.0 Hz
        sample_rate_out: float | None = GGWAVE_UNSET,  # Default: 48000.0 Hz
        sample_rate: float | None = GGWAVE_UNSET,  # Default: 48000.0 Hz
        samples_per_frame: int | None = GGWAVE_UNSET,  # Default: 1024
        sound_marker_threshold: float | None = GGWAVE_UNSET,  # Default: 3.0
        sample_format_inp: SampleFormat | None = GGWAVE_UNSET,  # Default: F32
        sample_format_out: SampleFormat | None = GGWAVE_UNSET,  # Default: F32
        operating_mode: OperatingMode | None = GGWAVE_UNSET,  # Default: RX_AND_TX
        *,
        enable_log: bool = False,
        **kwargs,
    ):
        """Initializes a GGWave instance.

        Args:
            payload_length: The length of the transmitted payload (-1 for variable length).
            sample_rate_inp: Input sample rate in Hz.
            sample_rate_out: Output sample rate in Hz.
            sample_rate: Operating sample rate in Hz.
            samples_per_frame: Number of samples per frame for FFT analysis.
            sound_marker_threshold: Threshold for detecting sound markers.
            sample_format_inp: Format of the input audio samples.
            sample_format_out: Format of the output audio samples.
            operating_mode: Specifies whether GGWave will transmit, receive, or both.
            enable_log: Enables internal GGWave logging (prints debug output).
            kwargs: Any additional parameters that may be supported in the future.

        """
        if GGWave._instances_count >= GGWave.MAX_INSTANCES:
            raise RuntimeError('Maximum number of GGWave instances reached (4).')

        if enable_log:
            self.enable_log()
        else:
            self.disable_log()

        # Get default parameters and update them
        self.parameters = ggwave.getDefaultParameters()
        updates = {
            'payloadLength': payload_length,
            'sampleRateInp': sample_rate_inp,
            'sampleRateOut': sample_rate_out,
            'sampleRate': sample_rate,
            'samplesPerFrame': samples_per_frame,
            'soundMarkerThreshold': sound_marker_threshold,
            'sampleFormatInp': sample_format_inp,
            'sampleFormatOut': sample_format_out,
            'operatingMode': operating_mode,
        }

        # Apply user-defined values if they are set
        self.parameters.update(
            {k: v for k, v in updates.items() if v is not GGWAVE_UNSET},
        )
        self.parameters.update(kwargs)

        # Create GGWave instance
        self.instance = ggwave.init(self.parameters)
        GGWave._instances_count += 1

    def __del__(self):
        self.free()

    def free(self):
        """Frees the GGWave instance and releases resources."""
        if self.instance is not None:
            ggwave.free(self.instance)
            self.instance = None
            GGWave._instances_count -= 1

    def encode(
        self,
        payload: str | bytes,
        protocol: ProtocolId = ProtocolId.AUDIBLE_NORMAL,
        volume: int = 10,
    ) -> bytes:
        """Encodes a given payload into an audio waveform."""
        if not payload:
            return b''
        return (
            ggwave.encode(
                payload,
                protocolId=protocol.value,
                volume=volume,
                instance=self.instance,
            )
            or b''
        )

    def decode(self, waveform: bytes) -> bytes:
        """Decodes an audio waveform into the original data, if successful."""
        if not waveform:
            return b''
        return ggwave.decode(self.instance, waveform) or b''

    @staticmethod
    def disable_log():
        """Disables GGWave internal logging."""
        ggwave.disableLog()

    @staticmethod
    def enable_log():
        """Enables GGWave internal logging."""
        ggwave.enableLog()

    @classmethod
    def toggle_rx_protocol(cls, protocol: ProtocolId, state: bool):
        """Enables or disables a specific reception (Rx) protocol.

        This allows restricting the number of decoding protocols,
        which can help reduce false positives and improve accuracy.
        """
        ggwave.rxToggleProtocol(protocol.value, int(state))

    @classmethod
    def toggle_tx_protocol(cls, protocol: ProtocolId, state: bool):
        """Enables or disables a specific transmission (Tx) protocol.

        Disabling unused protocols can reduce memory usage.
        """
        ggwave.txToggleProtocol(protocol.value, int(state))
