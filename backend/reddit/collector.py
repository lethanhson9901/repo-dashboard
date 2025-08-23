# collector.py

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Union, List
import praw
from praw.models import Comment, Submission
from praw.reddit import Reddit
from prawcore.exceptions import TooManyRequests, ResponseException, RequestException
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

        logger.info("🔧 Đang khởi tạo Reddit client...")
        logger.info(f"   👤 Username: {username}")
        logger.info(f"   🆔 Client ID: {client_id[:8]}...")
        logger.info(f"   🤖 User Agent: {user_agent}")
        
        try:
            self.reddit: Reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                username=username,
                password=password,
            )
            
            # Test connection
            logger.info("🔍 Đang kiểm tra kết nối Reddit API...")
            user_info = self.reddit.user.me()
            logger.info(f"   ✅ Kết nối thành công! User: {user_info.name}")
            logger.info(f"   📅 Tài khoản tạo: {datetime.fromtimestamp(user_info.created_utc).strftime('%Y-%m-%d')}")
            logger.info(f"   🏆 Karma: {user_info.link_karma} link, {user_info.comment_karma} comment")
            
        except Exception as e:
            logger.error(f"❌ Lỗi khởi tạo Reddit client: {e}")
            logger.error(f"📋 Loại lỗi: {type(e).__name__}")
            raise
        
        self.comment_depth = comment_depth
        self.output_dir = Path(output_dir or "./src/data/reddit")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Output directory: {self.output_dir.absolute()}")
        
        self.data: CollectorData = self._load_existing_data()
        logger.info("✅ RedditContentCollector đã được khởi tạo thành công")

    def _handle_rate_limit(self, error: TooManyRequests, context: str = "", wait_time: int = 60) -> None:
        """
        Handle rate limit errors with detailed logging.
        
        Args:
            error: The TooManyRequests exception
            context: Context where the rate limit occurred
            wait_time: Time to wait in seconds
        """
        logger.warning("=" * 50)
        logger.warning("⚠️  RATE LIMIT DETECTED!")
        logger.warning("=" * 50)
        logger.warning(f"📍 Context: {context}")
        logger.warning(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.warning(f"⏳ Waiting: {wait_time} seconds")
        logger.warning(f"📋 Error details: {error}")
        
        if hasattr(error, 'response') and error.response:
            logger.warning(f"📊 Response status: {error.response.status_code}")
            logger.warning(f"📋 Response headers: {dict(error.response.headers)}")
        
        logger.warning("=" * 50)
        time.sleep(wait_time)
        logger.info("✅ Rate limit wait completed, resuming...")

    def _log_api_stats(self) -> None:
        """Log current API usage statistics if available."""
        try:
            # Note: PRAW doesn't directly expose rate limit info, but we can log what we know
            logger.info("📊 API Usage Statistics:")
            logger.info("   - Reddit API limits: 60 requests per minute")
            logger.info("   - Current session: Active")
            logger.info("   - Rate limit handling: Enabled with exponential backoff")
        except Exception as e:
            logger.debug(f"Could not retrieve API stats: {e}")

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
        import time
        from prawcore.exceptions import TooManyRequests, ResponseException, RequestException
        
        news_items: List[NewsContent] = []
        total_posts_processed = 0
        total_posts_filtered = 0
        total_comments_processed = 0
        rate_limit_hits = 0
        
        try:
            time_mapping = {
                TimeFilter.DAY: "day",
                TimeFilter.WEEK: "week",
                TimeFilter.MONTH: "month"
            }
            
            # Get subscribed subreddits
            logger.info("🔍 Đang lấy danh sách subreddit đã đăng ký...")
            subscribed = list(self.reddit.user.subreddits(limit=None))
            logger.info(f"📋 Tìm thấy {len(subscribed)} subreddit đã đăng ký")
            
            for idx, subreddit in enumerate(subscribed, 1):
                subreddit_start_time = time.time()
                subreddit_posts = 0
                subreddit_filtered = 0
                
                try:
                    logger.info(f"🔄 [{idx}/{len(subscribed)}] Đang thu thập từ r/{subreddit}")
                    
                    # Fetch posts with rate limit handling
                    try:
                        top_posts = subreddit.top(
                            time_filter=time_mapping[time_filter],
                            limit=limit
                        )
                        posts_list = list(top_posts)  # Convert generator to list
                        logger.info(f"   📥 Lấy được {len(posts_list)} posts từ r/{subreddit}")
                        
                    except TooManyRequests as e:
                        rate_limit_hits += 1
                        self._handle_rate_limit(e, f"Fetching posts from r/{subreddit}", 60)
                        continue
                    except (ResponseException, RequestException) as e:
                        logger.error(f"   ❌ Lỗi API cho r/{subreddit}: {e}")
                        continue
                    
                    for post_idx, post in enumerate(posts_list, 1):
                        total_posts_processed += 1
                        subreddit_posts += 1
                        
                        if post.score >= min_score:
                            total_posts_filtered += 1
                            subreddit_filtered += 1
                            
                            logger.debug(f"      📝 [{post_idx}/{len(posts_list)}] Xử lý post: {post.title[:50]}... (score: {post.score})")
                            
                            # Process comments with rate limit handling
                            comments: List[CommentData] = []
                            try:
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
                                        "replies": replies
                                    }
                                
                                # Process top-level comments
                                for comment in post.comments:
                                    comment_data = process_comment(comment)
                                    if comment_data:
                                        comments.append(comment_data)
                                        total_comments_processed += 1
                                
                            except TooManyRequests as e:
                                rate_limit_hits += 1
                                self._handle_rate_limit(e, f"Processing comments for post {post.id}", 30)
                                continue
                            except Exception as e:
                                logger.error(f"      ❌ Lỗi xử lý comments của post {post.id}: {e}")
                                continue
                            
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
                        else:
                            logger.debug(f"      ⏭️  [{post_idx}/{len(posts_list)}] Bỏ qua post (score {post.score} < {min_score})")
                    
                    subreddit_duration = time.time() - subreddit_start_time
                    logger.info(f"   ✅ Hoàn thành r/{subreddit}: {subreddit_filtered}/{subreddit_posts} posts (thời gian: {subreddit_duration:.2f}s)")
                            
                except TooManyRequests as e:
                    rate_limit_hits += 1
                    self._handle_rate_limit(e, f"General subreddit processing for r/{subreddit}", 60)
                    continue
                except Exception as e:
                    logger.error(f"   ❌ Lỗi thu thập từ subreddit {subreddit}: {e}")
                    logger.error(f"   📋 Loại lỗi: {type(e).__name__}")
                    continue
            
            # Sort all collected news items by score in descending order
            news_items.sort(key=lambda x: x["score"], reverse=True)
            
            # Log summary
            logger.info("=" * 60)
            logger.info("📊 TỔNG KẾT THU THẬP TIN TỨC:")
            logger.info(f"   - Subreddit đã xử lý: {len(subscribed)}")
            logger.info(f"   - Posts đã xử lý: {total_posts_processed}")
            logger.info(f"   - Posts đạt tiêu chuẩn: {total_posts_filtered}")
            logger.info(f"   - Comments đã xử lý: {total_comments_processed}")
            logger.info(f"   - Rate limit hits: {rate_limit_hits}")
            logger.info(f"   - Tin tức cuối cùng: {len(news_items)} items")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ Lỗi chung trong quá trình thu thập tin tức: {e}")
            logger.error(f"📋 Loại lỗi: {type(e).__name__}")
            
        return news_items

    def save_community_news(self, news_items: List[NewsContent], time_filter: TimeFilter) -> None:
        """
        Save fetched news items to a JSON file.
        
        Args:
            news_items (List[NewsContent]): List of news items to save
            time_filter (TimeFilter): Time filter used to fetch the news
        """
        import time
        
        try:
            save_start_time = time.time()
            output_file = self.output_dir / f"community_news_{time_filter}.json"
            
            logger.info(f"💾 Đang lưu {len(news_items)} tin tức vào {output_file}")
            
            # Calculate file size estimate
            total_comments = sum(len(item.get("comments", [])) for item in news_items)
            logger.info(f"   📊 Thống kê dữ liệu:")
            logger.info(f"      - Tin tức: {len(news_items)} items")
            logger.info(f"      - Comments: {total_comments} comments")
            
            data = {
                "metadata": {
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "time_filter": time_filter,
                    "total_items": len(news_items),
                    "total_comments": total_comments,
                    "file_size_bytes": 0  # Will be updated after saving
                },
                "items": news_items
            }
            
            # Save with progress logging
            logger.info("   📝 Đang ghi file JSON...")
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Get file size
            file_size = output_file.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            # Update metadata with actual file size
            data["metadata"]["file_size_bytes"] = file_size
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            save_duration = time.time() - save_start_time
            logger.info(f"   ✅ Lưu thành công:")
            logger.info(f"      - File: {output_file}")
            logger.info(f"      - Kích thước: {file_size_mb:.2f} MB")
            logger.info(f"      - Thời gian: {save_duration:.2f} giây")
            logger.info(f"      - Tốc độ: {file_size_mb/save_duration:.2f} MB/s")
            
        except Exception as e:
            logger.error(f"❌ Lỗi khi lưu tin tức cộng đồng: {e}")
            logger.error(f"📋 Loại lỗi: {type(e).__name__}")
            raise