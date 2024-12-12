import os
import logging
from typing import Dict
from dotenv import load_dotenv
from collector import RedditContentCollector
from models import ContentType

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("backend/reddit/logs/reddit_collector.log", mode='a')
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
        load_dotenv()
    
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

def ensure_log_directory():
    """Ensure the log directory exists."""
    log_dir = "backend/reddit/logs"
    os.makedirs(log_dir, exist_ok=True)

def main() -> None:
    """Main entry point for the Reddit Content Collector."""
    try:
        # Ensure log directory exists
        ensure_log_directory()
        
        # Get environment variables
        env_vars = get_env_variables()
        
        collector = RedditContentCollector(
            client_id=env_vars["REDDIT_CLIENT_ID"],
            client_secret=env_vars["REDDIT_CLIENT_SECRET"],
            user_agent=env_vars["REDDIT_USER_AGENT"],
            username=env_vars["REDDIT_USERNAME"],
            password=env_vars["REDDIT_PASSWORD"],
            comment_depth=3
        )

        # Fetch new content
        logger.info("Fetching saved content...")
        new_saved = collector.get_content(ContentType.SAVED)
        logger.info(f"Found {len(new_saved)} new saved items")

        logger.info("Fetching upvoted content...")
        new_upvoted = collector.get_content(ContentType.UPVOTED)
        logger.info(f"Found {len(new_upvoted)} new upvoted items")

        # Generate web data
        logger.info("Generating web data...")
        collector.generate_web_data()
        logger.info("Data files have been updated")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    main()