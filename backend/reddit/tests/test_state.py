import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from backend.reddit.state import default_state, load_state, save_state


class StateTests(unittest.TestCase):
    def test_default_state_when_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "collector_state.json"
            state = load_state(state_path, subreddit_count=10)
            self.assertEqual(state["next_subreddit_index"], 0)
            self.assertEqual(state["subreddit_count"], 10)
            self.assertFalse(state["paused"])

    def test_save_and_reload_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "collector_state.json"
            state = default_state(subreddit_count=5)
            state["next_subreddit_index"] = 3
            state["paused"] = True
            save_state(state_path, state)
            reloaded = load_state(state_path, subreddit_count=5)
            self.assertEqual(reloaded["next_subreddit_index"], 3)
            self.assertTrue(reloaded["paused"])

    def test_reset_index_on_subreddit_change(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "collector_state.json"
            state = default_state(subreddit_count=100)
            state["next_subreddit_index"] = 99
            save_state(state_path, state)
            reloaded = load_state(state_path, subreddit_count=10)
            self.assertEqual(reloaded["next_subreddit_index"], 0)
            self.assertEqual(reloaded["subreddit_count"], 10)


if __name__ == "__main__":
    unittest.main()
