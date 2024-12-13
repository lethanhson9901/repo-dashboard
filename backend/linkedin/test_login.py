from linkedin_api import Linkedin
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import ssl
import time
import json
import re

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
BASE_PATH = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_PATH / ".env"
COOKIE_PATH = BASE_PATH / "linkedin_cookies.json"

class CustomHTTPAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

def create_session():
    """Create a requests session with retry logic"""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
    )
    
    adapter = CustomHTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    return session

def update_session_headers(session):
    """Update session headers with required LinkedIn API headers"""
    jsessionid = session.cookies.get('JSESSIONID', '').strip('"')
    
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
        'Accept-Language': 'en-US,en;q=0.9',
        'X-Li-Lang': 'en_US',
        'X-RestLi-Protocol-Version': '2.0.0',
        'X-Li-Page-Instance': 'urn:li:page:d_flagship3_profile_view_base;',
        'X-Li-Track': '{"clientVersion":"1.12.6","mpVersion":"1.12.6","osName":"web"}',
        'Csrf-Token': jsessionid,
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.linkedin.com/',
        'Origin': 'https://www.linkedin.com'
    })
    return session

def perform_login(session, username, password):
    """Perform manual login to LinkedIn"""
    try:
        # Get the login page first
        login_response = session.get('https://www.linkedin.com/login')
        if login_response.status_code != 200:
            logger.error("Failed to access login page")
            return False

        # Extract CSRF token
        csrf_pattern = r'name="loginCsrfParam" value="([^"]*)"'
        csrf_match = re.search(csrf_pattern, login_response.text)
        if not csrf_match:
            logger.error("Failed to extract CSRF token")
            return False
        
        csrf_token = csrf_match.group(1)

        # Prepare login data
        login_data = {
            'session_key': username,
            'session_password': password,
            'loginCsrfParam': csrf_token,
            'trk': 'guest_homepage-basic_nav-header-signin'
        }

        # Perform login
        auth_response = session.post(
            'https://www.linkedin.com/checkpoint/lg/login-submit',
            data=login_data,
            allow_redirects=True
        )

        # Check if we reached the feed
        if '/feed' in auth_response.url:
            logger.debug("Login successful")
            session = update_session_headers(session)
            return True

        logger.error(f"Login failed - unexpected redirect: {auth_response.url}")
        return False

    except Exception as e:
        logger.error(f"Login process failed: {e}")
        return False

def verify_authentication(session):
    """Verify authentication by checking miniProfile access"""
    try:
        # Try to access the mini profile endpoint
        profile_url = 'https://www.linkedin.com/voyager/api/me'
        
        # Add specific headers for this request
        headers = {
            'Accept': 'application/vnd.linkedin.normalized+json+2.1',
            'X-Requested-With': 'XMLHttpRequest',
            'X-RestLi-Protocol-Version': '2.0.0'
        }
        
        response = session.get(profile_url, headers=headers)
        
        if response.status_code == 200:
            logger.info("Successfully verified authentication")
            try:
                profile_data = response.json()
                logger.debug(f"Profile data received: {json.dumps(profile_data, indent=2)}")
            except json.JSONDecodeError:
                logger.warning("Could not parse profile data as JSON")
            return True
        else:
            logger.error(f"Failed to verify authentication. Status: {response.status_code}")
            if response.text:
                logger.debug(f"Response content: {response.text[:200]}...")
            return False
            
    except Exception as e:
        logger.error(f"Error verifying authentication: {e}")
        return False

def test_linkedin_login(username, password, max_retries=3):
    """Test LinkedIn login with retry logic and manual authentication"""
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            session = create_session()
            logger.info(f"Attempting to login with username: {username}")
            
            if perform_login(session, username, password):
                # Short delay before verification
                time.sleep(1)
                
                # Verify authentication
                if verify_authentication(session):
                    logger.info("Login test completed successfully")
                    return True
            
            retry_count += 1
            if retry_count < max_retries:
                wait_time = 2 ** retry_count
                logger.info(f"Retrying in {wait_time} seconds... (Attempt {retry_count + 1}/{max_retries})")
                time.sleep(wait_time)
                
        except Exception as e:
            logger.error(f"Login attempt failed: {str(e)}")
            logger.debug("Full exception details:", exc_info=True)
            retry_count += 1
            if retry_count < max_retries:
                wait_time = 2 ** retry_count
                logger.info(f"Retrying in {wait_time} seconds... (Attempt {retry_count + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                break
    
    logger.error("Max retries reached. Login failed.")
    return False

def main():
    try:
        load_dotenv(ENV_PATH)
        username = os.getenv('LINKEDIN_USERNAME')
        password = os.getenv('LINKEDIN_PASSWORD')
        
        if not username or not password:
            raise ValueError("LinkedIn credentials not found in environment variables")
        
        if test_linkedin_login(username, password):
            logger.info("Login test completed successfully")
        else:
            logger.error("Login test failed")
            
    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        logger.debug("Full exception details:", exc_info=True)
        raise

if __name__ == "__main__":
    main()