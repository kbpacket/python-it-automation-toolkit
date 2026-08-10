import unittest

from src.log_summary import summarize_lines


class LogSummaryTests(unittest.TestCase):
    def test_counts_levels_and_invalid_lines(self):
        lines = [
            "2026-08-10 10:00:00 INFO Started\n",
            "2026-08-10 10:01:00 ERROR Connection failed\n",
            "not a valid line\n",
        ]

        result = summarize_lines(lines)

        self.assertEqual(result["parsed_lines"], 2)
        self.assertEqual(result["invalid_lines"], 1)
        self.assertEqual(result["levels"], {"ERROR": 1, "INFO": 1})

    def test_keyword_match_is_case_insensitive(self):
        lines = [
            "2026-08-10 10:00:00 WARNING Authentication delayed\n",
            "2026-08-10 10:01:00 ERROR AUTHENTICATION failed\n",
        ]

        result = summarize_lines(lines, "authentication")

        self.assertEqual(result["keyword_matches"], 2)


if __name__ == "__main__":
    unittest.main()
