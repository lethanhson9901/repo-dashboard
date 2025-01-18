import os
import logging
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
    try:
        # Set up logging first
        setup_logging()
        logger.info("Starting Reddit news collection for last 24 hours...")
        
        # Get environment variables
        env_vars = get_env_variables()
        
        # Initialize collector with proper path handling
        output_dir = Path('src/data/reddit')

        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize collector
        collector = RedditContentCollector(
            client_id=env_vars["REDDIT_CLIENT_ID"],
            client_secret=env_vars["REDDIT_CLIENT_SECRET"],
            user_agent=env_vars["REDDIT_USER_AGENT"],
            username=env_vars["REDDIT_USERNAME"],
            password=env_vars["REDDIT_PASSWORD"],
            output_dir=output_dir,
            comment_depth=3
        )

        # Fetch only daily news
        logger.info("Fetching community news for the last 24 hours...")
        news_items = collector.get_community_news(
            time_filter=TimeFilter.DAY,
            min_score=5,     # Minimum score threshold
            limit=1000,      # Maximum number of posts to fetch
            comment_depth=3
        )
        collector.save_community_news(news_items, TimeFilter.DAY)
        logger.info(f"Found {len(news_items)} news items for the last 24 hours")
        logger.info("Daily news collection completed successfully")

    except Exception as e:
        logger.error(f"An error occurred while collecting news: {e}")
        raise

if __name__ == "__main__":
    main()