# Stream listening from the microphone
from ggwave_python import GGWave, waveform_utils

gg = GGWave()

try:
    print('Start listening...')
    for chunk in waveform_utils.listen():
        decoded = gg.decode(chunk)
        if decoded:
            print('Received:', decoded.decode('utf-8'))
finally:
    gg.free()
