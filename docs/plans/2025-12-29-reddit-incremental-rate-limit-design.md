# Reddit Incremental Collection + Rate Limit Design

## Goal
Collect community news across subscribed subreddits incrementally, stop before
rate limits, and resume on the next scheduled run. The state is committed so
GitHub Actions can pick up where it left off.

## Architecture
- State file: `src/data/reddit/collector_state.json`
- Incremental merge: `community_news_TimeFilter.DAY.json` is merged by post id
- Rate-limit awareness: use PRAW `reddit.auth.limits` (remaining/used/reset)
- Scheduler: a dedicated GitHub Actions workflow runs every 15 minutes

## Data Flow
1. Job starts and loads `collector_state.json`.
2. If paused and reset time has not passed, exit early.
3. Iterate subscribed subreddits starting from `next_subreddit_index`.
4. After each API batch, check rate limits:
   - If remaining <= threshold, persist state and exit.
5. Merge new news items into the existing JSON file.
6. When all subreddits complete, reset `next_subreddit_index` to 0 and mark
   `last_completed_at`.

## Error Handling
- `TooManyRequests`: mark paused, store reset timestamp, and exit without sleep.
- Network/API errors: log and skip the problematic subreddit, keep progress.
- Missing/corrupted state file: fall back to defaults and continue.

## Workflow
- New `reddit.yml` workflow triggers every 15 minutes and runs `get_news.py`.
- `deploy.yml` ignores pushes that only change `src/data/reddit/**` to avoid
  frequent builds; daily schedule still rebuilds the site.

## Testing
- Unit tests for state load/save behavior.
- Unit tests for news merge de-duplication.
- Manual smoke test with a small subreddit sample if needed.
