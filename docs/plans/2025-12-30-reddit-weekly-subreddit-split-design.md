# Reddit Weekly Split by Subreddit Design

## Goal
Collect weekly top posts with a hard cap of 50 posts per subreddit, and store
results in per-subreddit JSON files to keep data small and easy to inspect.

## Architecture
- Data output: `src/data/reddit/community_news/{subreddit}.json`
- Index file: `src/data/reddit/community_news/index.json`
- No aggregate `community_news_TimeFilter.WEEK.json` updates
- Incremental merge still keyed by post id

## Data Flow
1. Crawl weekly top posts as usual.
2. Group items by subreddit.
3. For each subreddit:
   - Load existing file if present
   - Merge by post id (new overwrites old)
   - Sort by score desc
   - Trim to 50 items
   - Write `{subreddit}.json`
4. Write `index.json` with subreddit list + counts.

## Error Handling
- Missing or invalid JSON files are treated as empty.
- Subreddit names are sanitized to safe filenames.

## UI Changes
- Reddit view loads `index.json` first.
- UI loads only the selected subreddit's file.
- "All Subreddits" view is removed to avoid large payloads.

## Scheduling
- `reddit.yml` cron updated to run every 60 minutes.
