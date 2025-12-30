# Reddit Weekly Subreddit Split Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Store weekly Reddit news as per-subreddit JSON files capped at 50 items each, with a small index file for the UI.

**Architecture:** Group news items by subreddit, merge incrementally by post id, trim to 50 per subreddit, and write `src/data/reddit/community_news/{subreddit}.json` plus `index.json`. UI loads the index and only the selected subreddit file.

**Tech Stack:** Python (PRAW, stdlib), React (Vite), GitHub Actions.

### Task 1: Subreddit file helpers + tests

**Files:**
- Create: `backend/reddit/subreddit_news.py`
- Create: `backend/reddit/tests/test_subreddit_news.py`

**Step 1: Write the failing test**

```python
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "backend" / "reddit"))
sys.path.insert(0, str(ROOT))

from backend.reddit.subreddit_news import (
    sanitize_subreddit_name,
    group_by_subreddit,
    trim_top_posts,
    build_index_entries,
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
        trimmed = trim_top_posts(items, limit=50)
        self.assertEqual(len(trimmed), 50)
        self.assertEqual(trimmed[0]["score"], 59)

    def test_build_index_entries(self):
        grouped = {"one": [{"id": "a"}], "two": [{"id": "b"}, {"id": "c"}]}
        entries = build_index_entries(grouped)
        entry_map = {entry["subreddit"]: entry["total_items"] for entry in entries}
        self.assertEqual(entry_map["one"], 1)
        self.assertEqual(entry_map["two"], 2)


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest discover -s backend/reddit/tests -p "test_subreddit_news.py" -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'backend.reddit.subreddit_news'`

**Step 3: Write minimal implementation**

```python
import re
from typing import Dict, List


def sanitize_subreddit_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "_", name)


def group_by_subreddit(items: List[Dict]) -> Dict[str, List[Dict]]:
    grouped: Dict[str, List[Dict]] = {}
    for item in items:
        subreddit = item.get("subreddit", "unknown")
        grouped.setdefault(subreddit, []).append(item)
    return grouped


def trim_top_posts(items: List[Dict], limit: int) -> List[Dict]:
    return sorted(items, key=lambda item: item.get("score", 0), reverse=True)[:limit]


def build_index_entries(grouped: Dict[str, List[Dict]]) -> List[Dict]:
    entries = []
    for subreddit, items in grouped.items():
        entries.append({
            "subreddit": subreddit,
            "file": f"{sanitize_subreddit_name(subreddit)}.json",
            "total_items": len(items),
        })
    return sorted(entries, key=lambda entry: entry["subreddit"].lower())
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest discover -s backend/reddit/tests -p "test_subreddit_news.py" -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add backend/reddit/subreddit_news.py backend/reddit/tests/test_subreddit_news.py
git commit -m "feat: add subreddit news helpers"
```

### Task 2: Save weekly news by subreddit + index

**Files:**
- Modify: `backend/reddit/collector.py`
- Modify: `backend/reddit/get_news.py`

**Step 1: Write the failing test**

```python
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "backend" / "reddit"))
sys.path.insert(0, str(ROOT))

from backend.reddit.collector import RedditContentCollector
from backend.reddit.models import TimeFilter


class SaveBySubredditTests(unittest.TestCase):
    def test_save_by_subreddit_creates_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
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
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest discover -s backend/reddit/tests -p "test_save_by_subreddit.py" -v`  
Expected: FAIL with `AttributeError: 'RedditContentCollector' object has no attribute 'save_community_news_by_subreddit'`

**Step 3: Write minimal implementation**

```python
from subreddit_news import (
    build_index_entries,
    group_by_subreddit,
    sanitize_subreddit_name,
    trim_top_posts,
)

    def save_community_news_by_subreddit(self, news_items: List[NewsContent], time_filter: TimeFilter) -> None:
        output_dir = self.output_dir / "community_news"
        output_dir.mkdir(parents=True, exist_ok=True)
        grouped = group_by_subreddit(news_items)
        index_entries = []
        for subreddit, items in grouped.items():
            file_name = f"{sanitize_subreddit_name(subreddit)}.json"
            output_file = output_dir / file_name
            existing_items = []
            if output_file.exists():
                try:
                    with output_file.open("r", encoding="utf-8") as f:
                        existing_items = json.load(f).get("items", [])
                except Exception:
                    existing_items = []

            merged_items = merge_news_items(existing_items, items)
            trimmed_items = trim_top_posts(merged_items, limit=50)
            total_comments = sum(len(item.get("comments", [])) for item in trimmed_items)
            data = {
                "metadata": {
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "time_filter": time_filter,
                    "subreddit": subreddit,
                    "total_items": len(trimmed_items),
                    "total_comments": total_comments,
                    "file_size_bytes": 0,
                },
                "items": trimmed_items,
            }
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            file_size = output_file.stat().st_size
            data["metadata"]["file_size_bytes"] = file_size
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            index_entries.append({
                "subreddit": subreddit,
                "file": file_name,
                "total_items": len(trimmed_items),
                "last_updated": data["metadata"]["last_updated"],
            })

        index = {
            "metadata": {
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "time_filter": time_filter,
                "total_subreddits": len(index_entries),
            },
            "items": sorted(index_entries, key=lambda entry: entry["subreddit"].lower()),
        }
        with (output_dir / "index.json").open("w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
```

**Step 4: Update `get_news.py` to call new save method and set limit to 50**

```python
        logger.info("📊 Thông số thu thập:")
        logger.info(f"   - Time filter: {time_filter}")
        logger.info(f"   - Min score: 3")
        logger.info(f"   - Limit: 50 posts")

        news_items = collector.get_community_news(
            time_filter=time_filter,
            min_score=3,
            limit=50,
            comment_depth=3,
            state_path=state_path,
            rate_limit_threshold=5
        )
        collector.save_community_news_by_subreddit(news_items, time_filter)
```

**Step 5: Run test to verify it passes**

Run: `python -m unittest discover -s backend/reddit/tests -p "test_save_by_subreddit.py" -v`  
Expected: PASS

**Step 6: Commit**

```bash
git add backend/reddit/collector.py backend/reddit/get_news.py backend/reddit/tests/test_save_by_subreddit.py
git commit -m "feat: save weekly news per subreddit"
```

### Task 3: Update Reddit UI to use subreddit index

**Files:**
- Modify: `src/components/Reddit/index.jsx`

**Step 1: Write manual verification checklist**
- Open Reddit view with `showType = news`
- Ensure subreddit dropdown loads from `index.json`
- Selecting a subreddit loads its file and renders posts
- If no subreddit selected, show a placeholder prompt

**Step 2: Implement UI changes**

```jsx
const subredditModules = import.meta.glob('../../data/reddit/community_news/*.json');

// When showType === 'news'
const index = await import('../../data/reddit/community_news/index.json');
setSubredditIndex(index.items || []);
setSelectedSubreddit(index.items?.[0]?.subreddit || '');

// On subreddit selection
const file = subredditIndex.find(item => item.subreddit === selectedSubreddit)?.file;
const module = subredditModules[`../../data/reddit/community_news/${file}`];
if (module) {
  const data = await module();
  setPosts(data.items || []);
  setMetadata(data.metadata || null);
}
```

**Step 3: Manual verification**
- Run `npm run dev`
- Navigate to Reddit view
- Select multiple subreddits and confirm data swaps

**Step 4: Commit**

```bash
git add src/components/Reddit/index.jsx
git commit -m "feat: load reddit news by subreddit index"
```

### Task 4: Update Reddit workflow schedule

**Files:**
- Modify: `.github/workflows/reddit.yml`

**Step 1: Update cron**

```yaml
on:
  schedule:
    - cron: "0 * * * *"
```

**Step 2: Commit**

```bash
git add .github/workflows/reddit.yml
git commit -m "ci: run reddit workflow hourly"
```
