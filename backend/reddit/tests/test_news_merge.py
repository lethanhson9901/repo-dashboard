import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from backend.reddit.news_merge import merge_news_items


class NewsMergeTests(unittest.TestCase):
    def test_merge_keeps_all_ids(self):
        existing = [{"id": "a", "title": "A"}]
        new = [{"id": "b", "title": "B"}]
        merged = merge_news_items(existing, new)
        ids = {item["id"] for item in merged}
        self.assertEqual(ids, {"a", "b"})

    def test_merge_prefers_new_item(self):
        existing = [{"id": "a", "title": "Old"}]
        new = [{"id": "a", "title": "New"}]
        merged = merge_news_items(existing, new)
        self.assertEqual(merged[0]["title"], "New")


if __name__ == "__main__":
    unittest.main()
