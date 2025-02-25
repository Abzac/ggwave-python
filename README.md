# GGWave Python Wrapper

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

A Python wrapper for GGWave, a data-over-sound communication library.

## 📌 Features
- Encode and decode messages using sound waves.
- Support for multiple transmission protocols.
- Optional real-time audio transmission and reception via PyAudio.

## 🚀 Installation

### Basic installation
```sh
pip install ggwave
```

### With audio support (PyAudio)
```sh
pip install ggwave[audio]
```

## 🔧 Usage

### Encoding and decoding messages
```python
from ggwave import GGWave, ProtocolId

gg = GGWave()
try:
    waveform = gg.encode("Hello, world!", ProtocolId.AUDIBLE_FAST, volume=20)
    decoded = gg.decode(waveform)
    print(decoded.decode("utf-8"))  # "Hello, world!"
finally:
    gg.free()
```

### Real-time audio transmission (requires PyAudio)
```python
gg = GGWave()
try:
    waveform = gg.encode("Test message", ProtocolId.AUDIBLE_FAST, volume=20)
    gg.play_waveform(waveform)
finally:
    gg.free()
```

### Real-time audio reception
```python
gg = GGWave()
try:
    for message in gg.listen():
        print("Received:", message.decode("utf-8"))
finally:
    gg.free()
```

## ⚙️ Technical Details
GGWave transmits data using **frequency-shift keying (FSK)**, allowing devices to communicate via sound. The transmission rate is **8-16 bytes/sec**, depending on the selected protocol. 

## How to run tests

Install pytest

```sh
pip install pytest
```

Run all tests

```sh
pytest tests/
```

Run a single test

```
pytest tests/test_ggwave.py -k test_encode_decode
```

## 📝 License
This project is licensed under the MIT License.
