# models.py
from datetime import datetime
from typing import TypedDict, List, Dict, Union
from enum import Enum

class ContentType(str, Enum):
    """Enum for content types to ensure type safety."""
    SAVED = "saved"
    UPVOTED = "upvoted"

class CommentData(TypedDict):
    """Type definition for comment data."""
    id: str
    author: str
    text: str
    score: int
    created_utc: str
    is_submitter: bool
    replies: List['CommentData']

class RedditContent(TypedDict):
    """Type definition for Reddit content items."""
    id: str
    title: str
    type: str
    subreddit: str
    url: str
    author: str
    created_utc: str
    score: int
    text: str
    comments: List[CommentData]

class SubredditStats(TypedDict):
    """Type definition for subreddit statistics."""
    saved: int
    upvoted: int

class Metadata(TypedDict):
    """Type definition for metadata."""
    last_updated: str
    total_saved: int
    total_upvoted: int
    subreddits: Dict[str, SubredditStats]

class CollectorData(TypedDict):
    """Type definition for collector data."""
    saved: List[RedditContent]
    upvoted: List[RedditContent]
    metadata: Metadata
    

class TimeFilter(str, Enum):
    """Enum for time filtering options."""
    DAY = "day"
    THREE_DAYS = "3days"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

class NewsContent(TypedDict):
    """Type definition for news content with enhanced details."""
    id: str
    title: str
    subreddit: str
    url: str
    author: str
    created_utc: str
    score: int
    num_comments: int
    upvote_ratio: float
    text: str                    # Full post content
    is_original_content: bool
    link_flair_text: Union[str, None]
    permalink: str               # Full Reddit permalink
    domain: str                 # Source domain for links
    is_self: bool              # Whether it's a self post
    comments: List[CommentData] # Full comment thread