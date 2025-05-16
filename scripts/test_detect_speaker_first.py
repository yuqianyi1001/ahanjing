import os
import unittest

from detect_speaker_first import ask_grok_ai, MAX_CHARS, T0099_DIR

class TestDetectSpeakerFirst(unittest.TestCase):
    def test_0307_md(self):
        fname = "0307.md"
        fpath = os.path.join(T0099_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
        result = ask_grok_ai(content)
        # The expected answer is "disciple" because a 比丘 asks the Buddha first
        self.assertEqual(result, "disciple", f"Expected 'disciple', got '{result}'")

if __name__ == "__main__":
    unittest.main()
