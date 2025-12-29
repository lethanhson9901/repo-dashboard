# Reddit Incremental Collection and Rate Limit Throttling Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add incremental subreddit collection with rate-limit-aware pausing and a 15-minute Reddit workflow that resumes via committed state.

**Architecture:** Persist progress in `src/data/reddit/collector_state.json`, merge new items into the existing news JSON, and stop early when `reddit.auth.limits` shows low remaining quota or a reset timer. A dedicated GitHub Actions workflow updates Reddit data without triggering a build.

**Tech Stack:** Python (PRAW, stdlib), GitHub Actions.

### Task 1: State helpers for incremental progress

**Files:**
- Create: `backend/reddit/state.py`
- Modify: `backend/reddit/models.py`
- Test: `backend/reddit/tests/test_state.py`

**Step 1: Write the failing test**

```python
import json
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
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest discover -s backend/reddit/tests -p "test_state.py" -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'backend.reddit.state'`

**Step 3: Write minimal implementation**

```python
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


STATE_VERSION = 1


def default_state(subreddit_count: int) -> Dict[str, Any]:
    return {
        "version": STATE_VERSION,
        "next_subreddit_index": 0,
        "subreddit_count": subreddit_count,
        "paused": False,
        "pause_reason": "",
        "rate_remaining": None,
        "rate_used": None,
        "rate_reset_timestamp": None,
        "last_run_at": "",
        "last_completed_at": "",
    }


def load_state(path: Path, subreddit_count: int) -> Dict[str, Any]:
    state = default_state(subreddit_count)
    if not path.exists():
        return state

    try:
        with path.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)
    except Exception:
        return state

    for key in state:
        if key in loaded:
            state[key] = loaded[key]

    if not isinstance(state["next_subreddit_index"], int):
        state["next_subreddit_index"] = 0
    if state["next_subreddit_index"] < 0 or state["next_subreddit_index"] >= subreddit_count:
        state["next_subreddit_index"] = 0

    state["subreddit_count"] = subreddit_count
    return state


def save_state(path: Path, state: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=False, indent=2)
```

**Step 4: Update models for type hints**

```python
class CollectorState(TypedDict):
    version: int
    next_subreddit_index: int
    subreddit_count: int
    paused: bool
    pause_reason: str
    rate_remaining: Union[int, None]
    rate_used: Union[int, None]
    rate_reset_timestamp: Union[float, None]
    last_run_at: str
    last_completed_at: str
```

**Step 5: Run test to verify it passes**

Run: `python -m unittest discover -s backend/reddit/tests -p "test_state.py" -v`  
Expected: PASS

**Step 6: Commit**

```bash
git add backend/reddit/state.py backend/reddit/models.py backend/reddit/tests/test_state.py
git commit -m "feat: add reddit collector state helpers"
```

### Task 2: News merge helpers for incremental save

**Files:**
- Create: `backend/reddit/news_merge.py`
- Test: `backend/reddit/tests/test_news_merge.py`

**Step 1: Write the failing test**

```python
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
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest discover -s backend/reddit/tests -p "test_news_merge.py" -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'backend.reddit.news_merge'`

**Step 3: Write minimal implementation**

```python
from typing import Dict, List


def merge_news_items(existing: List[Dict], new: List[Dict]) -> List[Dict]:
    merged = {item["id"]: item for item in existing}
    for item in new:
        merged[item["id"]] = item
    return list(merged.values())
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest discover -s backend/reddit/tests -p "test_news_merge.py" -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add backend/reddit/news_merge.py backend/reddit/tests/test_news_merge.py
git commit -m "feat: add reddit news merge helper"
```

### Task 3: Incremental collection with rate-limit-aware pausing

**Files:**
- Modify: `backend/reddit/collector.py`
- Modify: `backend/reddit/get_news.py`

**Step 1: Add rate-limit helpers to collector**

```python
    def _get_rate_limits(self) -> Dict[str, Union[int, float, None]]:
        limits = getattr(self.reddit.auth, "limits", {}) or {}
        remaining = limits.get("remaining")
        used = limits.get("used")
        reset_timestamp = limits.get("reset_timestamp")
        if reset_timestamp is None:
            reset_seconds = limits.get("reset")
            if reset_seconds is not None:
                reset_timestamp = time.time() + float(reset_seconds)
        return {
            "remaining": remaining,
            "used": used,
            "reset_timestamp": reset_timestamp,
        }

    def _should_pause(self, threshold: int) -> Dict[str, Union[int, float, None]]:
        limits = self._get_rate_limits()
        remaining = limits.get("remaining")
        if remaining is None:
            return {}
        if remaining <= threshold:
            return limits
        return {}
```

**Step 2: Replace `get_community_news` with incremental logic**

```python
    def get_community_news(
        self,
        time_filter: TimeFilter = TimeFilter.DAY,
        min_score: int = 10,
        limit: int = 500,
        comment_depth: int = 3,
        state_path: Union[str, Path, None] = None,
        rate_limit_threshold: int = 5,
    ) -> List[NewsContent]:
        news_items: List[NewsContent] = []
        total_posts_processed = 0
        total_posts_filtered = 0
        total_comments_processed = 0
        rate_limit_hits = 0

        time_mapping = {
            TimeFilter.DAY: "day",
            TimeFilter.WEEK: "week",
            TimeFilter.MONTH: "month",
        }

        logger.info("🔍 Đang lấy danh sách subreddit đã đăng ký...")
        subscribed = list(self.reddit.user.subreddits(limit=None))
        logger.info(f"📋 Tìm thấy {len(subscribed)} subreddit đã đăng ký")

        state_file = Path(state_path) if state_path else (self.output_dir / "collector_state.json")
        state = load_state(state_file, len(subscribed))
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state["last_run_at"] = now

        reset_timestamp = state.get("rate_reset_timestamp")
        if state.get("paused") and reset_timestamp and time.time() < reset_timestamp:
            logger.warning("⏸️  Đang tạm dừng do rate limit, sẽ thử lại ở lần chạy sau.")
            save_state(state_file, state)
            return []

        state["paused"] = False
        state["pause_reason"] = ""

        paused = False
        start_index = state["next_subreddit_index"]
        for idx in range(start_index, len(subscribed)):
            subreddit = subscribed[idx]
            subreddit_start_time = time.time()
            subreddit_posts = 0
            subreddit_filtered = 0

            logger.info(f"🔄 [{idx + 1}/{len(subscribed)}] Đang thu thập từ r/{subreddit}")

            try:
                top_posts = subreddit.top(
                    time_filter=time_mapping[time_filter],
                    limit=limit,
                )
                posts_list = list(top_posts)
                logger.info(f"   📥 Lấy được {len(posts_list)} posts từ r/{subreddit}")
            except TooManyRequests as e:
                rate_limit_hits += 1
                limits = self._get_rate_limits()
                state.update({
                    "paused": True,
                    "pause_reason": "too_many_requests",
                    "rate_remaining": limits.get("remaining"),
                    "rate_used": limits.get("used"),
                    "rate_reset_timestamp": limits.get("reset_timestamp"),
                    "next_subreddit_index": idx,
                })
                save_state(state_file, state)
                break
            except (ResponseException, RequestException) as e:
                logger.error(f"   ❌ Lỗi API cho r/{subreddit}: {e}")
                state["next_subreddit_index"] = idx + 1
                save_state(state_file, state)
                continue

            limits = self._should_pause(rate_limit_threshold)
            if limits:
                state.update({
                    "paused": True,
                    "pause_reason": "low_remaining_after_list",
                    "rate_remaining": limits.get("remaining"),
                    "rate_used": limits.get("used"),
                    "rate_reset_timestamp": limits.get("reset_timestamp"),
                    "next_subreddit_index": idx,
                })
                save_state(state_file, state)
                paused = True
                break

            for post_idx, post in enumerate(posts_list, 1):
                total_posts_processed += 1
                subreddit_posts += 1

                if post.score < min_score:
                    continue

                total_posts_filtered += 1
                subreddit_filtered += 1

                comments: List[CommentData] = []
                try:
                    post.comments.replace_more(limit=0)

                    def process_comment(comment, depth=0) -> CommentData:
                        if depth >= comment_depth or not hasattr(comment, "body"):
                            return None
                        replies = []
                        if hasattr(comment, "replies"):
                            for reply in comment.replies:
                                reply_data = process_comment(reply, depth + 1)
                                if reply_data:
                                    replies.append(reply_data)
                        return {
                            "id": comment.id,
                            "author": str(comment.author) if comment.author else "[deleted]",
                            "text": comment.body,
                            "score": comment.score,
                            "created_utc": datetime.fromtimestamp(comment.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                            "is_submitter": comment.is_submitter,
                            "replies": replies,
                        }

                    for comment in post.comments:
                        comment_data = process_comment(comment)
                        if comment_data:
                            comments.append(comment_data)
                            total_comments_processed += 1

                except TooManyRequests:
                    rate_limit_hits += 1
                    limits = self._get_rate_limits()
                    state.update({
                        "paused": True,
                        "pause_reason": "too_many_requests_comments",
                        "rate_remaining": limits.get("remaining"),
                        "rate_used": limits.get("used"),
                        "rate_reset_timestamp": limits.get("reset_timestamp"),
                        "next_subreddit_index": idx,
                    })
                    save_state(state_file, state)
                    paused = True
                    break
                except Exception as e:
                    logger.error(f"      ❌ Lỗi xử lý comments của post {post.id}: {e}")
                    continue

                news_items.append({
                    "id": post.id,
                    "title": post.title,
                    "subreddit": str(post.subreddit),
                    "url": post.url,
                    "author": str(post.author) if post.author else "[deleted]",
                    "created_utc": datetime.fromtimestamp(post.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "upvote_ratio": post.upvote_ratio,
                    "text": post.selftext if post.is_self else "[External Link]",
                    "is_original_content": post.is_original_content,
                    "link_flair_text": post.link_flair_text,
                    "permalink": f"https://reddit.com{post.permalink}",
                    "domain": post.domain,
                    "is_self": post.is_self,
                    "comments": comments,
                })

                limits = self._should_pause(rate_limit_threshold)
                if limits:
                    state.update({
                        "paused": True,
                        "pause_reason": "low_remaining_after_post",
                        "rate_remaining": limits.get("remaining"),
                        "rate_used": limits.get("used"),
                        "rate_reset_timestamp": limits.get("reset_timestamp"),
                        "next_subreddit_index": idx,
                    })
                    save_state(state_file, state)
                    paused = True
                    break

            subreddit_duration = time.time() - subreddit_start_time
            logger.info(f"   ✅ Hoàn thành r/{subreddit}: {subreddit_filtered}/{subreddit_posts} posts (thời gian: {subreddit_duration:.2f}s)")

            if paused:
                break

            state["next_subreddit_index"] = idx + 1
            save_state(state_file, state)

        if not paused:
            state["next_subreddit_index"] = 0
            state["paused"] = False
            state["last_completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_state(state_file, state)

        news_items.sort(key=lambda x: x["score"], reverse=True)
        logger.info("=" * 60)
        logger.info("📊 TỔNG KẾT THU THẬP TIN TỨC:")
        logger.info(f"   - Subreddit đã xử lý: {len(subscribed)}")
        logger.info(f"   - Posts đã xử lý: {total_posts_processed}")
        logger.info(f"   - Posts đạt tiêu chuẩn: {total_posts_filtered}")
        logger.info(f"   - Comments đã xử lý: {total_comments_processed}")
        logger.info(f"   - Rate limit hits: {rate_limit_hits}")
        logger.info(f"   - Tin tức cuối cùng: {len(news_items)} items")
        logger.info("=" * 60)

        return news_items
```

**Step 3: Update `save_community_news` to merge**

```python
from news_merge import merge_news_items

        output_file = self.output_dir / f"community_news_{time_filter}.json"
        existing_items: List[NewsContent] = []
        if output_file.exists():
            try:
                with output_file.open("r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                    existing_items = existing_data.get("items", [])
            except Exception:
                existing_items = []

        merged_items = merge_news_items(existing_items, news_items)
        merged_items.sort(key=lambda x: x["score"], reverse=True)
        total_comments = sum(len(item.get("comments", [])) for item in merged_items)

        data = {
            "metadata": {
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "time_filter": time_filter,
                "total_items": len(merged_items),
                "total_comments": total_comments,
                "file_size_bytes": 0,
            },
            "items": merged_items,
        }
```

**Step 4: Update `get_news.py` to pass state and threshold**

```python
        state_path = output_dir / "collector_state.json"
        news_items = collector.get_community_news(
            time_filter=TimeFilter.DAY,
            min_score=3,
            limit=1000,
            comment_depth=3,
            state_path=state_path,
            rate_limit_threshold=5,
        )
```

**Step 5: Manual smoke test**

Run: `python backend/reddit/get_news.py`  
Expected: log shows state file updates and stops early if remaining quota is low.

**Step 6: Commit**

```bash
git add backend/reddit/collector.py backend/reddit/get_news.py
git commit -m "feat: add incremental reddit collection with rate limit pause"
```

### Task 4: GitHub Actions scheduling for 15-minute runs

**Files:**
- Create: `.github/workflows/reddit.yml`
- Modify: `.github/workflows/deploy.yml`

**Step 1: Add Reddit workflow**

```yaml
name: Update Reddit Data
on:
  schedule:
    - cron: "*/15 * * * *"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  fetch-reddit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.x"
      - run: |
          sudo apt-get update
          sudo apt-get install -y libxml2-dev libxslt1-dev
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Fetch Reddit data
        env:
          REDDIT_CLIENT_ID: ${{ secrets.REDDIT_CLIENT_ID }}
          REDDIT_CLIENT_SECRET: ${{ secrets.REDDIT_CLIENT_SECRET }}
          REDDIT_USERNAME: ${{ secrets.REDDIT_USERNAME }}
          REDDIT_PASSWORD: ${{ secrets.REDDIT_PASSWORD }}
        run: |
          mkdir -p src/data/reddit
          python backend/reddit/get_news.py
      - name: Commit and push changes
        run: |
          git config --global user.name 'GitHub Actions Bot'
          git config --global user.email 'actions@github.com'
          git add src/data/reddit/
          git diff --quiet && git diff --staged --quiet || (git commit -m "[ci run]: Update reddit data" && git push)
```

**Step 2: Update deploy workflow to ignore Reddit-only pushes**

```yaml
on:
  push:
    branches: [ main ]
    paths-ignore:
      - "src/data/reddit/**"
```

**Step 3: Remove Reddit fetch job and artifact usage**

- Delete job `fetch-reddit` from `.github/workflows/deploy.yml`.
- Update `combine-and-commit` job `needs` to `[fetch-github]`.
- Remove the “Download reddit data” step from `combine-and-commit`.

**Step 4: Commit**

```bash
git add .github/workflows/reddit.yml .github/workflows/deploy.yml
git commit -m "ci: add 15-min reddit workflow and skip reddit-only pushes"
```
