from ggwave_python import GGWave, ProtocolId, wav_utils

gg = GGWave()

try:
    # 1. Encoding into WAV
    waveform = gg.encode('Hello, world!', ProtocolId.AUDIBLE_FAST, volume=20)
    sample_rate, sample_format, channels = wav_utils.ggwave_to_waveform_params(gg)
    wav_bytes = wav_utils.waveform_to_wav(
        waveform,
        sample_rate,
        sample_format,
        channels,
    )

    # 2. Playing WAV
    wav_utils.play_wav(wav_bytes)

    # 3. Saving WAV into file
    with open('hello.wav', 'wb') as f:
        f.write(wav_bytes)

    # 4. Loading WAV from file
    with open('hello.wav', 'rb') as f:
        wav_bytes = f.read()

    # 4. Decoding back
    recovered_waveform, _, _ = wav_utils.wav_to_waveform(wav_bytes, sample_format)
    decoded = gg.decode(recovered_waveform)
    print(decoded.decode('utf-8'))  # "Hello, world!"

finally:
    gg.free()
