import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "backend" / "reddit"))
sys.path.insert(0, str(ROOT))

from backend.reddit.collector import RedditContentCollector
from backend.reddit.models import TimeFilter


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
            items = [
                {"id": "a", "subreddit": "one", "score": 10, "comments": []},
                {"id": "b", "subreddit": "two", "score": 5, "comments": []},
            ]
            collector.save_community_news_by_subreddit(items, TimeFilter.WEEK)
            self.assertTrue((Path(tmpdir) / "community_news" / "one.json").exists())
            self.assertTrue((Path(tmpdir) / "community_news" / "two.json").exists())
            self.assertTrue((Path(tmpdir) / "community_news" / "index.json").exists())


if __name__ == "__main__":
    unittest.main()
