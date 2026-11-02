import unittest
from daily_agent import normalize, too_similar, MIX


class DailyAgentTests(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize("Hello, World!"), "hello world")

    def test_near_duplicate(self):
        self.assertTrue(too_similar("how do you design frontend?", ["How do you design frontend?!"]))
        self.assertFalse(too_similar("coffee after a football match", ["How do you design frontend?"]))

    def test_mix(self):
        self.assertGreaterEqual(len(set(MIX[:6])), 5)


if __name__ == "__main__":
    unittest.main()
