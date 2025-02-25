# Stream listening (commented out for manual testing)
from ggwave_python import GGWave

gg = GGWave()
try:
    for chunk in gg.listen():
        print("Received chunk:", chunk)
finally:
    gg.free()
