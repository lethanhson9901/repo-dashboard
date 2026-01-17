import re
from datetime import datetime, timedelta
from typing import Dict, List


def sanitize_subreddit_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "_", name)


def group_by_subreddit(items: List[Dict]) -> Dict[str, List[Dict]]:
    grouped: Dict[str, List[Dict]] = {}
    for item in items:
        subreddit = item.get("subreddit", "unknown")
        grouped.setdefault(subreddit, []).append(item)
    return grouped


def filter_recent_posts(items: List[Dict], days: int = 7) -> List[Dict]:
    cutoff = datetime.utcnow() - timedelta(days=days)
    recent_items: List[Dict] = []
    for item in items:
        created_str = item.get("created_utc")
        if not created_str:
            continue
        try:
            created_at = datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        if created_at >= cutoff:
            recent_items.append(item)
    return recent_items


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
