# Vercel daily cron deployment (GitHub data) - design

Date: 2026-01-31
Owner: son

## Overview
Move deployment off GitHub Actions and serve GitHub data directly on Vercel using a daily cron job and an API route. The UI will fetch data from `/api/repos` instead of bundling `src/data/repos.json`. The API route will call the GitHub REST API (public, no token) and cache the response on Vercel CDN for 24 hours.

## Goals
- Remove dependency on GitHub Actions for data refresh.
- Fetch repository data directly from GitHub public API.
- Keep the solution free and simple to operate.
- Update data daily with predictable caching behavior.

## Non-goals
- No private data or GitHub PAT usage.
- No external storage requirement (KV/Blob/R2) unless needed later.
- No backend framework migration.

## Architecture
- **Vercel API route**: `/api/repos`
  - Fetches GitHub starred repos for `GH_USERNAME`.
  - Paginates through results (`per_page=100`) until empty page.
  - Maps data to the existing UI schema.
  - Returns JSON with CDN caching headers.
- **Vercel Cron**:
  - Daily schedule hits `/api/repos` to warm cache.
- **Frontend (Vite)**:
  - Fetches `/api/repos` on load.
  - Validates response with existing `validateRepoData`.
  - Shows loading, error, and empty states.

## Data flow
1. Daily cron (or first user visit) calls `/api/repos`.
2. API route requests GitHub `/users/{username}/starred` pages.
3. API returns normalized JSON and sets cache headers:
   - `Cache-Control: s-maxage=86400, stale-while-revalidate=3600`.
4. Frontend fetches `/api/repos` and renders dashboard.

## Error handling
- GitHub API error -> return 502 with short message.
- Invalid/missing `GH_USERNAME` -> return 500 with actionable message.
- Frontend displays a friendly error and retry action.

## Configuration
- **Env**: `GH_USERNAME` (required). Optional `ITEMS_PER_PAGE`.
- **Vercel**: add `vercel.json` cron schedule for daily execution.

## Testing and verification
- Local: `npm run dev`, verify UI loads data from `/api/repos`.
- Local API: `curl http://localhost:5173/api/repos` (or the Vite port) to inspect JSON.
- Vercel: call deployed `/api/repos` and confirm cache headers.

## Rollout notes
- Update README to describe Vercel deployment and env setup.
- Remove references to GitHub Actions data sync if no longer used.
