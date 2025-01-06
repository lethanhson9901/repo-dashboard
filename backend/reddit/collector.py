# collector.py

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Union, List
import praw
from praw.models import Comment, Submission
from praw.reddit import Reddit
from models import *

logger = logging.getLogger(__name__)


class RedditContentCollector:
    """Collect and process Reddit user content."""
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
        output_dir: Union[str, Path] = None,
        comment_depth: int = 3
    ) -> None:
        if not all([client_id, client_secret, user_agent, username, password]):
            raise ValueError("All Reddit API credentials must be provided")

        self.reddit: Reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )
        
        self.comment_depth = comment_depth
        self.output_dir = Path(output_dir or "./src/data/reddit")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data: CollectorData = self._load_existing_data()

    def _load_existing_data(self) -> CollectorData:
        """Load existing data from JSON file."""
        default_data: CollectorData = {
            "saved": [],
            "upvoted": [],
            "metadata": {
                "last_updated": "",
                "total_saved": 0,
                "total_upvoted": 0,
                "subreddits": {}
            }
        }

        json_path = self.output_dir / "reddit_content.json"
        try:
            if json_path.exists():
                with json_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return default_data

        return default_data

    def _process_comment(self, comment: Comment, depth: int = 0) -> CommentData:
        """Process a single comment and its replies up to max depth."""
        if not isinstance(comment, Comment):
            return None

        replies: List[CommentData] = []
        if depth < self.comment_depth and hasattr(comment, 'replies'):
            comment.replies.replace_more(limit=0)  # Remove MoreComments objects
            for reply in comment.replies:
                if isinstance(reply, Comment):
                    reply_data = self._process_comment(reply, depth + 1)
                    if reply_data:
                        replies.append(reply_data)

        return {
            "id": comment.id,
            "author": str(comment.author) if comment.author else "[deleted]",
            "text": comment.body if hasattr(comment, 'body') else "[No content]",
            "score": int(comment.score),
            "created_utc": datetime.fromtimestamp(comment.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
            "is_submitter": comment.is_submitter,
            "replies": replies
        }

    def _process_item(self, item: Union[Submission, Comment]) -> RedditContent:
        """Process a Reddit item into structured format."""
        is_submission = isinstance(item, Submission)
        
        text = "[External Link]"
        if is_submission and item.is_self:
            text = getattr(item, "selftext", "[No content]")
        elif isinstance(item, Comment):
            text = getattr(item, "body", "[No content]")

        content: RedditContent = {
            "id": item.id,
            "title": getattr(item, "title", "[Comment]"),
            "type": "post" if is_submission else "comment",
            "subreddit": str(item.subreddit),
            "url": f"https://reddit.com{item.permalink}",
            "author": str(item.author) if item.author else "[deleted]",
            "created_utc": datetime.fromtimestamp(item.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
            "score": int(item.score),
            "text": text,
            "comments": []
        }

        if is_submission:
            item.comments.replace_more(limit=0)  # Remove MoreComments objects
            for comment in item.comments:
                comment_data = self._process_comment(comment)
                if comment_data:
                    content["comments"].append(comment_data)

        return content

    def get_content(self, content_type: ContentType) -> List[RedditContent]:
        """Fetch content from Reddit account."""
        existing_ids = {item["id"] for item in self.data[content_type]}
        new_content: List[RedditContent] = []

        try:
            items = (self.reddit.user.me().saved(limit=None) if content_type == ContentType.SAVED
                    else self.reddit.user.me().upvoted(limit=None))

            for item in items:
                if item.id not in existing_ids:
                    content = self._process_item(item)
                    new_content.append(content)
                    self.data[content_type].append(content)

        except Exception as e:
            logger.error(f"Error fetching {content_type} content: {e}")

        return new_content

    def get_subreddit_stats(self) -> Dict[str, SubredditStats]:
        """Calculate subreddit statistics."""
        stats: Dict[str, SubredditStats] = {}
        
        for content_type in ContentType:
            for item in self.data[content_type]:
                subreddit = item["subreddit"]
                if subreddit not in stats:
                    stats[subreddit] = {"saved": 0, "upvoted": 0}
                stats[subreddit][content_type] += 1

        return stats

    def generate_web_data(self) -> None:
        """Generate and save JSON files."""
        try:
            self.data["metadata"].update({
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_saved": len(self.data["saved"]),
                "total_upvoted": len(self.data["upvoted"]),
                "subreddits": self.get_subreddit_stats()
            })

            output_path = self.output_dir / "reddit_content.json"
            print("data is written to: ", output_path)
            with output_path.open("w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"Error generating web data: {e}")
            raise
