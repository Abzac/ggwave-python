# Simple encoding/decoding example
from ggwave_python import GGWave, ProtocolId

gg = GGWave()
try:
    waveform = gg.encode("Hello, world!", ProtocolId.AUDIBLE_FAST, volume=20)
    decoded = gg.decode(waveform)
    gg.play_waveform(waveform)  # Optionally, play an encoded waveform
    print(decoded.decode("utf-8"))  # "Hello, world!"
finally:
    gg.free()
