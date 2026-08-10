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


    def test_merge_preserves_existing_comments_when_new_has_none(self):
        existing = [{"id": "a", "title": "A", "comments": [{"id": "c1", "text": "hello"}]}]
        new = [{"id": "a", "title": "A updated", "comments": []}]
        merged = merge_news_items(existing, new)
        self.assertEqual(merged[0]["title"], "A updated")
        self.assertEqual(len(merged[0]["comments"]), 1)
        self.assertEqual(merged[0]["comments"][0]["id"], "c1")

    def test_merge_uses_new_comments_when_present(self):
        existing = [{"id": "a", "title": "A", "comments": [{"id": "c1"}]}]
        new = [{"id": "a", "title": "A", "comments": [{"id": "c2"}, {"id": "c3"}]}]
        merged = merge_news_items(existing, new)
        self.assertEqual(len(merged[0]["comments"]), 2)
        self.assertEqual(merged[0]["comments"][0]["id"], "c2")


if __name__ == "__main__":
    unittest.main()
