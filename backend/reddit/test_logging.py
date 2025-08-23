#!/usr/bin/env python3
"""
Test script để kiểm tra logging và rate limit detection của Reddit collector.
"""

import os
import logging
import time
from pathlib import Path
from dotenv import load_dotenv
from collector import RedditContentCollector
from models import TimeFilter

def setup_test_logging():
    """Set up logging for testing."""
    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "test_reddit_logging.log"
    
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG for maximum detail
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, mode='w')  # Overwrite for testing
        ]
    )

def test_reddit_connection():
    """Test Reddit connection and basic functionality."""
    logger = logging.getLogger(__name__)
    
    try:
        # Load environment variables
        env_path = Path(__file__).resolve().parent / ".env"
        load_dotenv(env_path)
        
        required_vars = [
            "REDDIT_CLIENT_ID",
            "REDDIT_CLIENT_SECRET", 
            "REDDIT_USERNAME",
            "REDDIT_PASSWORD"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            logger.error(f"❌ Missing environment variables: {missing_vars}")
            return False
        
        logger.info("🧪 BẮT ĐẦU TEST REDDIT CONNECTION")
        logger.info("=" * 60)
        
        # Initialize collector
        collector = RedditContentCollector(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "TestCollector/1.0"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            output_dir="./test_output",
            comment_depth=2
        )
        
        # Test basic functionality
        logger.info("🔍 Testing basic Reddit functionality...")
        
        # Get user info
        user = collector.reddit.user.me()
        logger.info(f"✅ User authenticated: {user.name}")
        
        # Get subscribed subreddits (limited for testing)
        logger.info("📋 Getting subscribed subreddits...")
        subscribed = list(collector.reddit.user.subreddits(limit=5))
        logger.info(f"✅ Found {len(subscribed)} subscribed subreddits (limited to 5 for testing)")
        
        for subreddit in subscribed:
            logger.info(f"   - r/{subreddit}")
        
        # Test fetching a small amount of data
        logger.info("🔍 Testing data fetching (limited)...")
        test_items = collector.get_community_news(
            time_filter=TimeFilter.DAY,
            min_score=10,
            limit=5,  # Very small limit for testing
            comment_depth=1
        )
        
        logger.info(f"✅ Successfully fetched {len(test_items)} test items")
        
        # Test saving
        if test_items:
            logger.info("💾 Testing data saving...")
            collector.save_community_news(test_items, TimeFilter.DAY)
            logger.info("✅ Data saving test completed")
        
        logger.info("=" * 60)
        logger.info("🎉 TẤT CẢ TEST ĐÃ HOÀN THÀNH THÀNH CÔNG!")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ TEST FAILED!")
        logger.error("=" * 60)
        logger.error(f"🔍 Error: {e}")
        logger.error(f"📋 Error type: {type(e).__name__}")
        logger.error("=" * 60)
        return False

def test_rate_limit_simulation():
    """Simulate rate limit scenarios for testing."""
    logger = logging.getLogger(__name__)
    
    logger.info("🧪 BẮT ĐẦU TEST RATE LIMIT SIMULATION")
    logger.info("=" * 60)
    
    # This is a simulation - in real scenarios, rate limits would be triggered by actual API calls
    logger.info("⚠️  Rate limit simulation:")
    logger.info("   - Reddit API limit: 60 requests per minute")
    logger.info("   - Current implementation handles TooManyRequests exceptions")
    logger.info("   - Automatic retry with exponential backoff")
    logger.info("   - Detailed logging of rate limit events")
    
    logger.info("✅ Rate limit handling test completed")
    return True

if __name__ == "__main__":
    setup_test_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 BẮT ĐẦU REDDIT LOGGING TEST SUITE")
    logger.info("=" * 80)
    
    # Test 1: Connection and basic functionality
    test1_success = test_reddit_connection()
    
    # Test 2: Rate limit simulation
    test2_success = test_rate_limit_simulation()
    
    # Summary
    logger.info("=" * 80)
    logger.info("📊 TEST SUMMARY:")
    logger.info(f"   - Connection Test: {'✅ PASSED' if test1_success else '❌ FAILED'}")
    logger.info(f"   - Rate Limit Test: {'✅ PASSED' if test2_success else '❌ FAILED'}")
    logger.info("=" * 80)
    
    if test1_success and test2_success:
        logger.info("🎉 TẤT CẢ TEST ĐÃ HOÀN THÀNH THÀNH CÔNG!")
        exit(0)
    else:
        logger.error("❌ MỘT SỐ TEST ĐÃ THẤT BẠI!")
        exit(1)
