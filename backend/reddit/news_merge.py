from typing import Dict, List


def merge_news_items(existing: List[Dict], new: List[Dict]) -> List[Dict]:
    merged = {item["id"]: item for item in existing}
    for item in new:
        merged[item["id"]] = item
    return list(merged.values())
