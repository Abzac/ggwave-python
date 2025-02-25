import unittest

from ggwave_python import PYAUDIO_ENABLED, GGWave, ProtocolId


class TestGGWave(unittest.TestCase):
    def setUp(self):
        """Initialize a GGWave instance before each test."""
        self.gg = GGWave()

    def tearDown(self):
        """Cleanup GGWave instance after each test."""
        self.gg.free()

    def test_encode_decode(self):
        """Test encoding and decoding of a simple message."""
        message = "Hello, GGWave!"
        waveform = self.gg.encode(message, ProtocolId.AUDIBLE_FAST, volume=20)
        decoded = self.gg.decode(waveform)

        self.assertIsNotNone(decoded, "Decoded message should not be None")
        self.assertEqual(
            decoded.decode("utf-8"), message, "Decoded message should match original"
        )

    def test_empty_message(self):
        """Test encoding and decoding of an empty message."""
        waveform = self.gg.encode("", ProtocolId.AUDIBLE_FAST, volume=20)
        decoded = self.gg.decode(waveform)

        self.assertEqual(decoded, b"", "Decoded message should be empty")

    def test_invalid_waveform(self):
        """Test decoding an invalid waveform (should return None)."""
        invalid_waveform = b"\x00\x01\x02\x03\x04"
        decoded = self.gg.decode(invalid_waveform)

        self.assertIsNone(decoded, "Decoding invalid waveform should return None")

    @unittest.skipUnless(
        PYAUDIO_ENABLED, "PyAudio is not installed, skipping audio tests"
    )
    def test_play_waveform(self):
        """Test playing a waveform (should not raise an error)."""
        waveform = self.gg.encode("Test sound", ProtocolId.AUDIBLE_FAST, volume=20)
        try:
            self.gg.play_waveform(waveform)
        except Exception as e:
            self.fail(f"play_waveform raised an exception: {e}")

    @unittest.skipUnless(
        PYAUDIO_ENABLED, "PyAudio is not installed, skipping audio tests"
    )
    def test_listen_generator(self):
        """Test that the listen method is a generator."""
        gen = self.gg.listen()
        self.assertTrue(
            hasattr(gen, "__iter__") and hasattr(gen, "__next__"),
            "listen() should return a generator",
        )


if __name__ == "__main__":
    unittest.main()
