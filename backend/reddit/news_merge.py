from typing import Dict, List


def merge_news_items(existing: List[Dict], new: List[Dict]) -> List[Dict]:
    merged = {item["id"]: item for item in existing}
    for item in new:
        existing_item = merged.get(item["id"])
        if existing_item and not item.get("comments") and existing_item.get("comments"):
            item = {**item, "comments": existing_item["comments"]}
        merged[item["id"]] = item
    return list(merged.values())
