import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from typing import cast
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "backend" / "reddit"))
sys.path.insert(0, str(ROOT))

from backend.reddit.collector import RedditContentCollector
from backend.reddit.models import NewsContent, TimeFilter


class FakeUser:
    name = "tester"
    created_utc = 0
    link_karma = 0
    comment_karma = 0


class FakeReddit:
    def __init__(self):
        self.user = self

    def me(self):
        return FakeUser()


class SaveBySubredditTests(unittest.TestCase):
    def make_item(self, item_id: str, subreddit: str, score: int, created_utc: str) -> dict:
        return {
            "id": item_id,
            "title": f"title-{item_id}",
            "subreddit": subreddit,
            "url": f"https://example.com/{item_id}",
            "author": "tester",
            "created_utc": created_utc,
            "score": score,
            "num_comments": 0,
            "upvote_ratio": 1.0,
            "text": "",
            "is_original_content": False,
            "link_flair_text": None,
            "permalink": f"https://reddit.com/{item_id}",
            "domain": "example.com",
            "is_self": True,
            "comments": [],
        }

    def test_save_by_subreddit_creates_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("backend.reddit.collector.praw.Reddit", return_value=FakeReddit()):
                collector = RedditContentCollector(
                    client_id="x",
                    client_secret="y",
                    user_agent="z",
                    username="u",
                    password="p",
                    output_dir=Path(tmpdir),
                )
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            items = [
                self.make_item("a", "one", 10, now),
                self.make_item("b", "two", 5, now),
            ]
            collector.save_community_news_by_subreddit(cast(list[NewsContent], items), TimeFilter.WEEK)
            self.assertTrue((Path(tmpdir) / "community_news" / "one.json").exists())
            self.assertTrue((Path(tmpdir) / "community_news" / "two.json").exists())
            self.assertTrue((Path(tmpdir) / "community_news" / "index.json").exists())

    def test_save_by_subreddit_limits_and_filters(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("backend.reddit.collector.praw.Reddit", return_value=FakeReddit()):
                collector = RedditContentCollector(
                    client_id="x",
                    client_secret="y",
                    user_agent="z",
                    username="u",
                    password="p",
                    output_dir=Path(tmpdir),
                )

            recent_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            old_time = (datetime.utcnow() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")

            recent_items = [
                self.make_item(f"recent-{i}", "one", i, recent_time) for i in range(25)
            ]
            old_items = [
                self.make_item(f"old-{i}", "one", 100 + i, old_time) for i in range(5)
            ]

            collector.save_community_news_by_subreddit(
                cast(list[NewsContent], recent_items + old_items), TimeFilter.WEEK
            )

            output_file = Path(tmpdir) / "community_news" / "one.json"
            with output_file.open("r", encoding="utf-8") as f:
                data = json.load(f)

            items = data["items"]
            self.assertEqual(len(items), 20)
            self.assertTrue(all(item["created_utc"] == recent_time for item in items))
            self.assertTrue(all(item["id"].startswith("recent-") for item in items))


if __name__ == "__main__":
    unittest.main()
