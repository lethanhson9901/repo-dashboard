import os
import logging
import time
from typing import Dict
from pathlib import Path
from dotenv import load_dotenv
from collector import RedditContentCollector
from models import TimeFilter

# Get the script's directory
SCRIPT_DIR = Path(__file__).resolve().parent

# Set up logging
def setup_logging():
    """Set up logging configuration with proper path handling."""
    # Create logs directory relative to script location
    log_dir = SCRIPT_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "reddit_news.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, mode='a')
        ]
    )

logger = logging.getLogger(__name__)

def get_default_time_filter() -> TimeFilter:
    """Return the default time filter for community news."""
    return TimeFilter.WEEK

def get_time_filter_label(time_filter: TimeFilter) -> str:
    """Return a user-facing label for the selected time filter."""
    if time_filter == TimeFilter.WEEK:
        return "7 NGÀY QUA"
    if time_filter == TimeFilter.DAY:
        return "24 GIỜ QUA"
    return str(time_filter)

def get_news_post_limit() -> int:
    """Return the max posts to fetch per subreddit."""
    return 50

def get_env_variables() -> Dict[str, str]:
    """
    Get environment variables from either GitHub Actions secrets or .env file.
    Returns a dictionary of required environment variables.
    """
    # Try loading .env file if environment variables are not set
    if not os.getenv("REDDIT_CLIENT_ID"):
        env_path = SCRIPT_DIR / ".env"
        load_dotenv(env_path)
    
    # Define required variables with their environment variable names
    required_env_vars = {
        "REDDIT_CLIENT_ID": os.getenv("REDDIT_CLIENT_ID"),
        "REDDIT_CLIENT_SECRET": os.getenv("REDDIT_CLIENT_SECRET"),
        "REDDIT_USER_AGENT": os.getenv("REDDIT_USER_AGENT", "ContentCollector/1.0"),
        "REDDIT_USERNAME": os.getenv("REDDIT_USERNAME"),
        "REDDIT_PASSWORD": os.getenv("REDDIT_PASSWORD")
    }
    
    # Validate environment variables
    missing_vars = [k for k, v in required_env_vars.items() if not v]
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            "Please set them in GitHub Actions secrets or in a .env file"
        )
    
    return required_env_vars

def main() -> None:
    """Main entry point for fetching Reddit community news."""
    start_time = time.time()
    
    try:
        # Set up logging first
        setup_logging()
        time_filter = get_default_time_filter()
        time_label = get_time_filter_label(time_filter)
        logger.info("=" * 80)
        logger.info(f"🚀 BẮT ĐẦU THU THẬP TIN TỨC REDDIT - {time_label}")
        logger.info("=" * 80)
        
        # Get environment variables
        logger.info("📋 Đang kiểm tra biến môi trường...")
        env_vars = get_env_variables()
        logger.info("✅ Biến môi trường đã được cấu hình thành công")
        
        # Initialize collector with proper path handling
        output_dir = Path('src/data/reddit')
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Thư mục output: {output_dir.absolute()}")
        
        # Initialize collector
        logger.info("🔧 Đang khởi tạo RedditContentCollector...")
        collector = RedditContentCollector(
            client_id=env_vars["REDDIT_CLIENT_ID"],
            client_secret=env_vars["REDDIT_CLIENT_SECRET"],
            user_agent=env_vars["REDDIT_USER_AGENT"],
            username=env_vars["REDDIT_USERNAME"],
            password=env_vars["REDDIT_PASSWORD"],
            output_dir=output_dir,
            comment_depth=3
        )
        logger.info("✅ RedditContentCollector đã được khởi tạo thành công")

        # Fetch community news
        logger.info(f"🔍 BẮT ĐẦU THU THẬP TIN TỨC CỘNG ĐỒNG - {time_label}")
        logger.info("📊 Thông số thu thập:")
        logger.info(f"   - Time filter: {time_filter}")
        logger.info(f"   - Min score: 3")
        logger.info(f"   - Limit: {get_news_post_limit()} posts")
        logger.info(f"   - Comment depth: 3")
        
        fetch_start_time = time.time()
        state_path = output_dir / "collector_state.json"
        news_items = collector.get_community_news(
            time_filter=time_filter,
            min_score=3,     # Minimum score threshold
            limit=get_news_post_limit(),  # Maximum number of posts to fetch
            comment_depth=3,
            state_path=state_path,
            rate_limit_threshold=5
        )
        fetch_end_time = time.time()
        
        fetch_duration = fetch_end_time - fetch_start_time
        logger.info(f"⏱️  Thời gian thu thập: {fetch_duration:.2f} giây")
        logger.info(f"📈 Số lượng tin tức thu thập được: {len(news_items)} items")
        
        # Save the data
        logger.info("💾 Đang lưu dữ liệu...")
        save_start_time = time.time()
        collector.save_community_news_by_subreddit(news_items, time_filter)
        save_end_time = time.time()
        save_duration = save_end_time - save_start_time
        logger.info(f"⏱️  Thời gian lưu: {save_duration:.2f} giây")
        
        # Summary
        total_duration = time.time() - start_time
        logger.info("=" * 80)
        logger.info("✅ HOÀN THÀNH THU THẬP TIN TỨC REDDIT")
        logger.info("=" * 80)
        logger.info(f"📊 TỔNG KẾT:")
        logger.info(f"   - Tổng thời gian: {total_duration:.2f} giây")
        logger.info(f"   - Thời gian thu thập: {fetch_duration:.2f} giây")
        logger.info(f"   - Thời gian lưu: {save_duration:.2f} giây")
        logger.info(f"   - Số tin tức thu thập: {len(news_items)} items")
        logger.info(f"   - Tốc độ thu thập: {len(news_items)/fetch_duration:.2f} items/giây")
        logger.info("=" * 80)

    except Exception as e:
        total_duration = time.time() - start_time
        logger.error("=" * 80)
        logger.error("❌ LỖI TRONG QUÁ TRÌNH THU THẬP TIN TỨC")
        logger.error("=" * 80)
        logger.error(f"⏱️  Thời gian chạy trước khi lỗi: {total_duration:.2f} giây")
        logger.error(f"🔍 Chi tiết lỗi: {e}")
        logger.error(f"📋 Loại lỗi: {type(e).__name__}")
        logger.error("=" * 80)
        raise

if __name__ == "__main__":
    main()
