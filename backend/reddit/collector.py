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
    

    def get_community_news(
        self,
        time_filter: TimeFilter = TimeFilter.DAY,
        min_score: int = 10,
        limit: int = 500,
        comment_depth: int = 3  # Added parameter for comment depth
    ) -> List[NewsContent]:
        """
        Fetch detailed news from joined communities sorted by score.
        
        Args:
            time_filter (TimeFilter): Time filter for posts (day/week/month)
            min_score (int): Minimum score threshold for posts
            limit (int): Maximum number of posts to fetch
            comment_depth (int): How deep to go in comment threads
            
        Returns:
            List[NewsContent]: List of detailed news posts
        """
        news_items: List[NewsContent] = []
        
        try:
            time_mapping = {
                TimeFilter.DAY: "day",
                TimeFilter.WEEK: "week",
                TimeFilter.MONTH: "month"
            }
            
            # Get subscribed subreddits
            subscribed = list(self.reddit.user.subreddits(limit=None))
            logger.info(f"Found {len(subscribed)} subscribed subreddits")
            
            for subreddit in subscribed:
                try:
                    logger.info(f"Fetching from r/{subreddit}")
                    top_posts = subreddit.top(
                        time_filter=time_mapping[time_filter],
                        limit=limit
                    )
                    
                    for post in top_posts:
                        if post.score >= min_score:
                            # Process comments
                            comments: List[CommentData] = []
                            post.comments.replace_more(limit=0)  # Remove MoreComments objects
                            
                            def process_comment(comment, depth=0) -> CommentData:
                                if depth >= comment_depth or not hasattr(comment, 'body'):
                                    return None
                                    
                                replies = []
                                if hasattr(comment, 'replies'):
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
                                    # "subreddit": str(comment.subreddit),
                                    # "permalink": f"https://reddit.com{comment.permalink}",
                                    "replies": replies
                                }
                            
                            # Process top-level comments
                            for comment in post.comments:
                                comment_data = process_comment(comment)
                                if comment_data:
                                    comments.append(comment_data)
                            
                            # Create news item with enhanced details
                            news_item: NewsContent = {
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
                                "comments": comments
                            }
                            news_items.append(news_item)
                            
                except Exception as e:
                    logger.error(f"Error fetching from subreddit {subreddit}: {e}")
                    continue
            
            # Sort all collected news items by score in descending order
            news_items.sort(key=lambda x: x["score"], reverse=True)
            
        except Exception as e:
            logger.error(f"Error fetching community news: {e}")
            
        return news_items

    def save_community_news(self, news_items: List[NewsContent], time_filter: TimeFilter) -> None:
        """
        Save fetched news items to a JSON file.
        
        Args:
            news_items (List[NewsContent]): List of news items to save
            time_filter (TimeFilter): Time filter used to fetch the news
        """
        try:
            output_file = self.output_dir / f"community_news_{time_filter}.json"
            
            data = {
                "metadata": {
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "time_filter": time_filter,
                    "total_items": len(news_items)
                },
                "items": news_items
            }
            
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Saved {len(news_items)} news items to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving community news: {e}")
            raise