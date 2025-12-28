from linkedin_api import Linkedin
import json
from datetime import datetime
import requests
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
import ssl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
BASE_PATH = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_PATH / ".env"

class CustomHTTPAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        # Use secure default SSL configuration
        kwargs['ssl_context'] = ssl.create_default_context()
        return super().init_poolmanager(*args, **kwargs)

def create_session():
    """
    Create a requests session with retry logic and custom SSL configuration
    """
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=5,  # number of retries
        backoff_factor=1,  # wait 1, 2, 4, 8, 16 seconds between retries
        status_forcelist=[429, 500, 502, 503, 504],  # status codes to retry on
        allowed_methods=["HEAD", "GET", "POST"]
    )
    
    # Use custom adapter with modified SSL configuration
    adapter = CustomHTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    return session

def load_environment():
    """
    Load environment variables from .env file
    """
    if not ENV_PATH.exists():
        raise FileNotFoundError(f"Environment file not found at {ENV_PATH}")
    
    load_dotenv(ENV_PATH)
    
    username = os.getenv('LINKEDIN_USERNAME')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    if not username or not password:
        raise ValueError("LinkedIn credentials not found in environment variables")
    
    return username, password

def get_linkedin_saved_posts(username, password, max_retries=3):
    """
    Retrieve saved posts from LinkedIn with retry logic
    """
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Initialize custom session
            session = create_session()
            
            # Initialize the API client with custom session
            api = Linkedin(username, password)
            api.client.session = session
            
            # Test connection with a simple request
            try:
                profile = api.get_profile()
                logger.info("Successfully connected to LinkedIn")
            except Exception as e:
                logger.error(f"Failed to verify connection: {e}")
                raise
            
            # Get saved posts
            saved_posts = api.get_saved_posts()
            logger.info(f"Successfully retrieved {len(saved_posts)} posts from LinkedIn")
            
            # Process posts...
            formatted_posts = []
            for post in saved_posts:
                try:
                    images = []
                    if 'images' in post:
                        for img in post['images']:
                            if 'url' in img:
                                images.append(img['url'])
                    
                    if 'media' in post:
                        for media in post['media']:
                            if media.get('type') == 'image':
                                images.append(media.get('url', ''))
                    
                    post_data = {
                        'title': post.get('title', 'No title'),
                        'author': post.get('author', {}).get('name', 'Unknown'),
                        'date_saved': datetime.fromtimestamp(
                            post.get('saved_time', 0) / 1000
                        ).strftime('%Y-%m-%d %H:%M:%S'),
                        'url': f"https://www.linkedin.com/post/{post.get('id')}",
                        'content': post.get('commentary', {}).get('text', 'No content'),
                        'images': images,
                        'engagement': {
                            'likes': post.get('social', {}).get('totalLikes', 0),
                            'comments': post.get('social', {}).get('totalComments', 0)
                        }
                    }
                    formatted_posts.append(post_data)
                except Exception as e:
                    logger.error(f"Error processing post: {e}")
                    continue
            
            return formatted_posts
            
        except requests.exceptions.SSLError as e:
            logger.error(f"SSL Error: {e}")
            retry_count += 1
            if retry_count < max_retries:
                wait_time = 2 ** retry_count  # Exponential backoff
                logger.info(f"Retrying in {wait_time} seconds... (Attempt {retry_count + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise Exception("Max retries reached for SSL connection")
                
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection Error: {e}")
            retry_count += 1
            if retry_count < max_retries:
                wait_time = 2 ** retry_count
                logger.info(f"Retrying in {wait_time} seconds... (Attempt {retry_count + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise Exception("Max retries reached for connection")
                
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

def download_images(posts, output_dir=None):
    """
    Download images from posts to local directory
    
    Parameters:
    posts (list): List of formatted posts
    output_dir (str): Directory to save images (default: BASE_PATH/linkedin_images)
    """
    if output_dir is None:
        output_dir = BASE_PATH / 'linkedin_images'
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, post in enumerate(posts):
        for j, img_url in enumerate(post['images']):
            try:
                session = create_session()
                response = session.get(img_url)
                response.raise_for_status()
                
                # Create filename from post index and image index
                filename = f"post_{i+1}_image_{j+1}.jpg"
                filepath = output_dir / filename
                
                filepath.write_bytes(response.content)
                
                # Update image URL in post data to local path
                post['images'][j] = str(filepath)
                logger.info(f"Downloaded: {filename}")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error downloading image: {e}")
            finally:
                session.close()

def save_posts_to_file(posts, filename=None):
    """
    Save the retrieved posts to a JSON file
    
    Parameters:
    posts (list): List of formatted posts
    filename (str): Output filename (default: BASE_PATH/linkedin_saved_posts.json)
    """
    if filename is None:
        filename = BASE_PATH / 'linkedin_saved_posts.json'
    
    filepath = Path(filename)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with filepath.open('w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved posts to {filepath}")
    
    except Exception as e:
        logger.error(f"Error saving posts to file: {e}")
        raise

def validate_saved_data(filepath):
    """
    Validate that the saved data is complete and readable
    
    Parameters:
    filepath (Path): Path to the saved JSON file
    
    Returns:
    bool: True if validation passes, False otherwise
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            logger.error("Saved data is not in the expected format (list)")
            return False
            
        if not data:
            logger.warning("Saved data is empty")
            return False
            
        logger.info(f"Successfully validated saved data: {len(data)} posts")
        return True
        
    except Exception as e:
        logger.error(f"Error validating saved data: {e}")
        return False

def cleanup_old_files(directory, max_age_days=7):
    """
    Clean up old image files and JSON data
    
    Parameters:
    directory (Path): Directory to clean
    max_age_days (int): Maximum age of files to keep
    """
    try:
        current_time = datetime.now().timestamp()
        max_age_seconds = max_age_days * 24 * 60 * 60
        
        for filepath in directory.glob('**/*'):
            if filepath.is_file():
                file_age = current_time - filepath.stat().st_mtime
                if file_age > max_age_seconds:
                    filepath.unlink()
                    logger.info(f"Removed old file: {filepath}")
                    
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

def main():
    try:
        # Load credentials from environment variables
        username, password = load_environment()
        
        # Clean up old files
        cleanup_old_files(BASE_PATH)
        
        # Get saved posts with retry logic
        posts = get_linkedin_saved_posts(username, password)
        
        if not posts:
            logger.warning("No posts were retrieved")
            return
        
        # Download images
        download_images(posts)
        
        # Save to file
        output_file = BASE_PATH / 'linkedin_saved_posts.json'
        save_posts_to_file(posts, output_file)
        
        # Validate saved data
        if not validate_saved_data(output_file):
            logger.error("Data validation failed")
            return
        
        # Display summary
        logger.info(f"Successfully processed {len(posts)} posts")
        
        if posts:
            logger.info("\nFirst post summary:")
            logger.info(f"Title: {posts[0]['title']}")
            logger.info(f"Author: {posts[0]['author']}")
            logger.info(f"Date Saved: {posts[0]['date_saved']}")
            logger.info(f"Number of images: {len(posts[0]['images'])}")
    
    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        raise
    finally:
        logger.info("Script execution completed")

if __name__ == "__main__":
    main()