import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "backend" / "reddit"))
sys.path.insert(0, str(ROOT))

from datetime import datetime, timedelta

from backend.reddit.subreddit_news import (
    sanitize_subreddit_name,
    group_by_subreddit,
    trim_top_posts,
    build_index_entries,
    filter_recent_posts,
)


class SubredditNewsTests(unittest.TestCase):
    def test_sanitize_subreddit_name(self):
        self.assertEqual(sanitize_subreddit_name("ChatGPT"), "ChatGPT")
        self.assertEqual(sanitize_subreddit_name("my/sub"), "my_sub")
        self.assertEqual(sanitize_subreddit_name("AI&ML"), "AI_ML")

    def test_group_by_subreddit(self):
        items = [
            {"id": "a", "subreddit": "one"},
            {"id": "b", "subreddit": "two"},
            {"id": "c", "subreddit": "one"},
        ]
        grouped = group_by_subreddit(items)
        self.assertEqual(len(grouped["one"]), 2)
        self.assertEqual(len(grouped["two"]), 1)

    def test_trim_top_posts(self):
        items = [{"id": str(i), "score": i} for i in range(60)]
        trimmed = trim_top_posts(items, limit=20)
        self.assertEqual(len(trimmed), 20)
        self.assertEqual(trimmed[0]["score"], 59)

    def test_filter_recent_posts(self):
        now = datetime.utcnow()
        recent_item = {
            "id": "recent",
            "score": 10,
            "created_utc": (now - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"),
        }
        old_item = {
            "id": "old",
            "score": 100,
            "created_utc": (now - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"),
        }
        missing_ts_item = {"id": "missing", "score": 5}
        filtered = filter_recent_posts([recent_item, old_item, missing_ts_item], days=7)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], "recent")

    def test_build_index_entries(self):
        grouped = {"one": [{"id": "a"}], "two": [{"id": "b"}, {"id": "c"}]}
        entries = build_index_entries(grouped)
        entry_map = {entry["subreddit"]: entry["total_items"] for entry in entries}
        self.assertEqual(entry_map["one"], 1)
        self.assertEqual(entry_map["two"], 2)


if __name__ == "__main__":
    unittest.main()
