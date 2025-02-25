# GGWave Python Wrapper

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![CI](https://github.com/Abzac/ggwave-python/actions/workflows/ci.yml/badge.svg)](https://github.com/Abzac/ggwave-python/actions)
[![PyPI](https://img.shields.io/pypi/v/ggwave-python.svg)](https://pypi.org/project/ggwave-python/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linter: Ruff](https://img.shields.io/badge/linter-ruff-orange.svg)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
[![Tests](https://img.shields.io/github/actions/workflow/status/Abzac/ggwave-python/ci.yml?label=tests&logo=pytest)](https://github.com/Abzac/ggwave-python/actions)

A Python wrapper for GGWave, a data-over-sound communication library.

This Python library is built on top of the existing **Python bindings** from the official 
[GGWave repository](https://github.com/ggerganov/ggwave/tree/master). 
However, the original bindings are minimal and lack usability features, 
so this wrapper provides a more **user-friendly** API with **enum support, 
streamlined encoding/decoding, and optional PyAudio integration**.

## 📌 Features
- Encode and decode messages using sound waves.
- Support for multiple transmission protocols.
- Optional real-time audio transmission and reception via PyAudio.

## 🚀 Installation

### Basic installation
```sh
pip install ggwave_python
```

### With audio support (PyAudio)
```sh
pip install ggwave_python[audio]
```

## 🔧 Usage

### Encoding and decoding messages
```python
from ggwave_python import GGWave, ProtocolId

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
from ggwave_python import GGWave, ProtocolId, waveform_utils

gg = GGWave()
try:
    waveform = gg.encode("Test message", ProtocolId.AUDIBLE_FAST, volume=20)
    waveform_utils.play_waveform(waveform)
finally:
    gg.free()
```

### Real-time audio reception
```python
from ggwave_python import GGWave, waveform_utils

gg = GGWave()
try:
    for message in waveform_utils.listen():
        print("Received:", message.decode("utf-8"))
finally:
    gg.free()
```

### WAV Tools

On how to convert waveforms into WAV-format and back, please see [WAV Example](examples/wav_example.py).

### More examples

For more examples please see [Examples](examples/).


## ⚙️ Technical Details
GGWave transmits data using **frequency-shift keying (FSK)**, allowing devices to communicate via sound. 
The transmission rate is **8-16 bytes/sec**, depending on the selected protocol. 


## 🛠️ Development and Code Formatting

This project follows **strict code style and formatting rules**, enforced via `pre-commit` hooks.  
We use the following tools:

- **[Ruff](https://github.com/astral-sh/ruff)** → Linter, import sorting, and lightweight formatter.
- **[Black](https://github.com/psf/black)** → Code auto-formatter.
- **[Pytest](https://pytest.org/)** → For unit testing.

### **🔧 Setting Up the Development Environment**
To ensure a consistent environment, **use `poetry shell`** instead of installing packages globally.

```sh
poetry shell  # Activate the virtual environment
make init     # Install all dependencies
```

---

### **✅ Linting and Formatting**
Our project **requires clean, formatted code**. Use `make check` to validate your code.

#### **Check code style (without modifying files)**
```sh
make check
```

#### **Fix code style issues automatically**
```sh
make fix
```

---

### **🛠 Pre-Commit Hooks (Mandatory)**
This project **requires** `pre-commit` hooks to ensure formatting and linting before commits.  
You **must** install the pre-commit hook before making changes.

#### **Install pre-commit hook**
```sh
pre-commit install
```

#### **Run pre-commit manually on all files**
```sh
make pre-commit
```

#### **Remove pre-commit hooks (if needed)**
```sh
pre-commit uninstall
```

---

## **🧪 Running Tests**
Tests are managed with `pytest`.  

#### **Run all tests**
```sh
make tests
```

#### **Run a specific test**
```sh
pytest tests/test_ggwave.py -k test_encode_decode
```

---

## **📜 Makefile for Development Workflow**
All development tasks can be executed via `make` commands.

| Command            | Description                                           |
|--------------------|-------------------------------------------------------|
| `make init`       | Install dependencies inside the virtual environment   |
| `make check`      | Run Ruff & Black in **check mode** (without changes)  |
| `make fix`        | Auto-fix code style issues with Black & Ruff          |
| `make tests`      | Run all tests with Pytest                             |
| `make build`      | Build the package using Poetry                        |
| `make pre-commit` | Run all pre-commit hooks manually                     |
| `make help`       | Show all available `make` commands                    |

Now your development workflow is **fully automated**! 🚀


## 📝 License
This project is licensed under the MIT License.
