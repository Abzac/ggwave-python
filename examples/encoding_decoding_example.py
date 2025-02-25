from ggwave_python import GGWave, ProtocolId, waveform_utils

gg = GGWave()

try:
    # Encoding
    waveform = gg.encode('Hello, world!', ProtocolId.AUDIBLE_FAST, volume=20)

    # Playing the waveform
    waveform_utils.play_waveform(waveform)

    # Decoding
    decoded = gg.decode(waveform)
    print(decoded.decode('utf-8'))  # "Hello, world!"
finally:
    gg.free()
