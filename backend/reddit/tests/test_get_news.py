import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "backend" / "reddit"))
sys.path.insert(0, str(ROOT))

from backend.reddit.get_news import (
    get_default_time_filter,
    get_time_filter_label,
    get_news_post_limit,
)
from backend.reddit.models import TimeFilter


class GetNewsTests(unittest.TestCase):
    def test_default_time_filter_is_week(self):
        self.assertEqual(get_default_time_filter(), TimeFilter.WEEK)

    def test_time_filter_label_week(self):
        self.assertEqual(get_time_filter_label(TimeFilter.WEEK), "7 NGÀY QUA")

    def test_news_post_limit_weekly(self):
        self.assertEqual(get_news_post_limit(), 50)


if __name__ == "__main__":
    unittest.main()
