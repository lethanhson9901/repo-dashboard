from pathlib import Path
import praw
from dotenv import load_dotenv
import os

# Load environment variables
BASE_PATH = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_PATH / ".env"
load_dotenv(ENV_PATH)

def test_reddit_login():
    # Get credentials
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")
    username = os.getenv("REDDIT_USERNAME")
    password = os.getenv("REDDIT_PASSWORD")

    # Print credentials (except password)
    print("Attempting login with:")
    print(f"Client ID: {client_id}")
    print(f"User Agent: {user_agent}")
    print(f"Username: {username}")
    print("Password: [hidden]")

    try:
        # Initialize Reddit instance with debug enabled
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
            check_for_async=False  # Add this line
        )
        
        # Test authentication
        print("\nTrying to authenticate...")
        user = reddit.user.me()
        print(f"Successfully logged in as: {user}")
        
        # Test if we can access basic info
        print("\nTrying to access karma...")
        print(f"Link Karma: {reddit.user.me().link_karma}")
        
    except Exception as e:
        print(f"\nLogin failed with error: {str(e)}")
        print("\nPlease verify:")
        print("1. Your Reddit account is not locked/restricted")
        print("2. You're using the correct password (try logging in via web browser)")
        print("3. Your app credentials match exactly with what's shown in Reddit's app settings")
        print("4. Your account doesn't have 2FA enabled")

if __name__ == "__main__":
    test_reddit_login()