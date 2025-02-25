from setuptools import find_packages, setup

setup(
    name="ggwave_python",
    version="0.1.0",
    description="A Python wrapper for GGWave – data-over-sound communication",
    author="Abzac",
    author_email="rapturec@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["ggwave"],
    extras_require={
        "audio": ["pyaudio"],
    },
    python_requires=">=3.8,<3.11",
)
