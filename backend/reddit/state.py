import json
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

    if subreddit_count <= 0:
        state["next_subreddit_index"] = 0
    elif state["next_subreddit_index"] < 0 or state["next_subreddit_index"] >= subreddit_count:
        state["next_subreddit_index"] = 0

    state["subreddit_count"] = subreddit_count
    return state


def save_state(path: Path, state: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=False, indent=2)
